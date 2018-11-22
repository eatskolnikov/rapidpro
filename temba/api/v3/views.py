from __future__ import absolute_import, unicode_literals

import json

from django import forms
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, JsonResponse
from django.db.models import Prefetch
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import csrf_exempt

from smartmin.views import SmartFormView

from temba.api.models import APIToken, api_token, DeviceToken
from temba.api.v1.views import ContactEndpoint as ContactEndpointV1, FlowStepEndpoint as FlowStepEndpointV1
from temba.api.v2.views import AuthenticateView as AuthenticateEndpointV2, RunsEndpoint as RunsEndpointV2
from temba.api.v2.views import WriteAPIMixin, BaseAPIView, ListAPIMixin
from temba.contacts.models import Contact
from temba.flows.models import Flow, FlowStart, FlowStep, RuleSet
from temba.orgs.models import get_user_orgs, Org
from temba.utils import str_to_bool

from .serializers import FlowRunReadSerializer
from ..tasks import send_account_manage_email_task


def get_apitoken_from_auth(auth, user):
    token = auth.split(' ')[-1]
    api_token = APIToken.objects.filter(key=token, user=user).only('org').first()
    return api_token if api_token else None


class AuthenticateView(AuthenticateEndpointV2):

    def form_valid(self, form, *args, **kwargs):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        role_code = form.cleaned_data.get('role')

        user = authenticate(username=username, password=password)
        if user and user.is_active:
            login(self.request, user)

            role = APIToken.get_role_from_code(role_code)

            if role:
                token = api_token(user)
                return JsonResponse(dict(token=token), safe=False)
            else:  # pragma: needs cover
                return HttpResponse(status=403)
        else:  # pragma: needs cover
            return HttpResponse(status=403)


class UserOrgsEndpoint(BaseAPIView, ListAPIMixin):
    """
    Provides the user's organizations and API tokens to use on Surveyor App
    """

    permission = 'orgs.org_api'

    def list(self, request, *args, **kwargs):
        user = request.user
        user_orgs = get_user_orgs(user)
        orgs = []

        role = APIToken.get_role_from_code('S')

        if role:
            for org in user_orgs:
                token = APIToken.get_or_create(org, user, role)
                orgs.append({'org': {'id': org.pk, 'name': org.name}, 'token': token.key})

        else:  # pragma: needs cover
            return HttpResponse(status=403)

        return JsonResponse(orgs, safe=False)


class ManageAccountsListEndpoint(BaseAPIView, ListAPIMixin):
    """
    Provides the users that are pending of approbation
    """

    permission = 'orgs.org_manage_accounts'

    def list(self, request, *args, **kwargs):
        user = request.user
        authorization_key = request.META.get('HTTP_AUTHORIZATION')

        api_token = get_apitoken_from_auth(authorization_key, user)
        org = api_token.org if api_token else None

        if not org:
            return HttpResponse(status=404)

        surveryors = org.surveyors.filter(is_active=False).order_by('username')
        users = []

        role = APIToken.get_role_from_code('S')

        if role:
            for user in surveryors:
                users.append({'username': user.username, 'id': user.id})

        else:  # pragma: needs cover
            return HttpResponse(status=403)

        return JsonResponse(users, safe=False)


class ManageAccountsActionEndpoint(BaseAPIView, WriteAPIMixin):
    """
    Action to approve or disapprove users
    """

    permission = 'orgs.org_manage_accounts'

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        action = kwargs.get('action')

        errors = []

        for item in body:
            user = User.objects.filter(id=int(item.get('id'))).first()
            if user and not user.is_active:
                user_email = user.email
                if action == 'approve':
                    user.is_active = True
                    user.save(update_fields=['is_active'])
                    message = _('Congrats! Your account is approved. Please log in to access your surveys.')
                else:
                    user.delete()
                    message = _('Sorry. Your account was not approved. If you think this was a mistake, please contact %s.' % request.user.email)

                send_account_manage_email_task.delay(user_email, message)
            else:
                errors.append(_('User ID %s not found or already is active' % item.get('id')))

        if errors:
            return JsonResponse({'errors': errors}, safe=False, status=400)
        else:
            return HttpResponse(status=202)


class DeviceTokenEndpoint(BaseAPIView, WriteAPIMixin):
    """
    Action to add device tokens to user
    """

    permission = 'orgs.org_api'

    def post(self, request, *args, **kwargs):
        body = json.loads(request.body)
        device_token = body.get('device_token', None)
        user = request.user

        if not device_token:
            return JsonResponse({'errors': [_('device_token field is required')]}, safe=False, status=400)

        errors = []

        try:
            device_token_args = dict(device_token=device_token,
                                     user=user)
            DeviceToken.get_or_create(**device_token_args)
        except Exception as e:
            errors.append(e.args)

        if errors:
            return JsonResponse({'errors': errors}, safe=False, status=400)
        else:
            return HttpResponse(status=202)


class ContactEndpoint(ContactEndpointV1):
    permission = 'contacts.contact_api'


class FlowStepEndpoint(FlowStepEndpointV1):
    permission = 'flows.flow_api'


class RunsEndpoint(RunsEndpointV2):
    """
    This endpoint allows you to fetch flow runs. A run represents a single contact's path through a flow and is created
    each time a contact is started in a flow.

    ## Listing Flow Runs

    A `GET` request returns the flow runs for your organization, filtering them as needed. Each
    run has the following attributes:

     * **id** - the ID of the run (int), filterable as `id`.
     * **flow** - the UUID and name of the flow (object), filterable as `flow` with UUID.
     * **contact** - the UUID and name of the contact (object), filterable as `contact` with UUID.
     * **submitted_by** - the first name and last name of the user that submitted (object), filterable as `submitted_by`.
     * **responded** - whether the contact responded (boolean), filterable as `responded`.
     * **path** - the contact's path through the flow nodes (array of objects)
     * **values** - values generated by rulesets in the flow (array of objects).
     * **created_on** - the datetime when this run was started (datetime).
     * **modified_on** - when this run was last modified (datetime), filterable as `before` and `after`.
     * **exited_on** - the datetime when this run exited or null if it is still active (datetime).
     * **exit_type** - how the run ended (one of "interrupted", "completed", "expired").

    Note that you cannot filter by `flow` and `contact` at the same time.

    Example:

        GET /api/v3/runs.json?flow=f5901b62-ba76-4003-9c62-72fdacc1b7b7

    Response is the list of runs on the flow, most recently modified first:

        {
            "next": "http://example.com/api/v3/runs.json?cursor=cD0yMDE1LTExLTExKzExJTNBM40NjQlMkIwMCUzRv",
            "previous": null,
            "results": [
            {
                "id": 12345678,
                "flow": {"uuid": "f5901b62-ba76-4003-9c62-72fdacc1b7b7", "name": "Favorite Color"},
                "contact": {"uuid": "d33e9ad5-5c35-414c-abd4-e7451c69ff1d", "name": "Bob McFlow"},
                "responded": true,
                "path": [
                    {"node": "27a86a1b-6cc4-4ae3-b73d-89650966a82f", "time": "2015-11-11T13:05:50.457742Z"},
                    {"node": "fc32aeb0-ac3e-42a8-9ea7-10248fdf52a1", "time": "2015-11-11T13:03:51.635662Z"},
                    {"node": "93a624ad-5440-415e-b49f-17bf42754acb", "time": "2015-11-11T13:03:52.532151Z"},
                    {"node": "4c9cb68d-474f-4b9a-b65e-c2aa593a3466", "time": "2015-11-11T13:05:57.576056Z"}
                ],
                "values": {
                    "color": {
                        "value": "blue",
                        "category": "Blue",
                        "node": "fc32aeb0-ac3e-42a8-9ea7-10248fdf52a1",
                        "time": "2015-11-11T13:03:51.635662Z"
                    },
                    "reason": {
                        "value": "Because it's the color of sky",
                        "category": "All Responses",
                        "node": "4c9cb68d-474f-4b9a-b65e-c2aa593a3466",
                        "time": "2015-11-11T13:05:57.576056Z"
                    }
                },
                "created_on": "2015-11-11T13:05:57.457742Z",
                "modified_on": "2015-11-11T13:05:57.576056Z",
                "exited_on": "2015-11-11T13:05:57.576056Z",
                "exit_type": "completed"
            },
            ...
        }
    """
    serializer_class = FlowRunReadSerializer

    def filter_queryset(self, queryset):
        params = self.request.query_params
        org = self.request.user.get_org()

        # filter by flow (optional)
        flow_uuid = params.get('flow')
        if flow_uuid:
            flow = Flow.objects.filter(org=org, uuid=flow_uuid, is_active=True).first()
            if flow:
                queryset = queryset.filter(flow=flow)
            else:
                queryset = queryset.filter(pk=-1)

        # filter by id (optional)
        run_id = self.get_int_param('id')
        if run_id:
            queryset = queryset.filter(id=run_id)

        # filter by submitted_by (optional)
        submitted_by = self.get_int_param('submitted_by')
        if submitted_by:
            queryset = queryset.filter(submitted_by=submitted_by)

        # filter by contact (optional)
        contact_uuid = params.get('contact')
        if contact_uuid:
            contact = Contact.objects.filter(org=org, is_test=False, is_active=True, uuid=contact_uuid).first()
            if contact:
                queryset = queryset.filter(contact=contact)
            else:
                queryset = queryset.filter(pk=-1)
        else:
            # otherwise filter out test contact runs
            test_contact_ids = list(Contact.objects.filter(org=org, is_test=True).values_list('pk', flat=True))
            queryset = queryset.exclude(contact__pk__in=test_contact_ids)

        # limit to responded runs (optional)
        if str_to_bool(params.get('responded')):
            queryset = queryset.filter(responded=True)

        # use prefetch rather than select_related for foreign keys to avoid joins
        queryset = queryset.prefetch_related(
            Prefetch('flow', queryset=Flow.objects.only('uuid', 'name', 'base_language')),
            Prefetch('contact', queryset=Contact.objects.only('uuid', 'name', 'language')),
            Prefetch('start', queryset=FlowStart.objects.only('uuid')),
            Prefetch('values'),
            Prefetch('values__ruleset', queryset=RuleSet.objects.only('uuid', 'label')),
            Prefetch('steps', queryset=FlowStep.objects.only('run', 'step_uuid', 'arrived_on').order_by('arrived_on'))
        )

        return self.filter_before_after(queryset, 'modified_on')


class CreateAccountView(SmartFormView):

    class RegisterForm(forms.Form):
        surveyor_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Surveyor Password'}))
        first_name = forms.CharField(help_text=_("Your first name"), widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
        last_name = forms.CharField(help_text=_("Your last name"), widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
        email = forms.EmailField(help_text=_("Your email address"), widget=forms.TextInput(attrs={'placeholder': 'Email'}))
        password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
                                   help_text=_("Your password, at least eight letters please"))

        def __init__(self, *args, **kwargs):
            super(CreateAccountView.RegisterForm, self).__init__(*args, **kwargs)

        def clean_surveyor_password(self):
            password = self.cleaned_data['surveyor_password']
            org = Org.objects.filter(surveyor_password=password).first()
            if not org:
                password_error = _("Invalid surveyor password, please check with your project leader and try again.")
                self.cleaned_data['password_error'] = password_error
                raise forms.ValidationError(password_error)
            self.cleaned_data['org'] = org
            return password

        def clean_email(self):
            email = self.cleaned_data.get('email')
            if email:
                if User.objects.filter(username__iexact=email):
                    email_error = _("That email address is already used")
                    self.cleaned_data['register_email_error'] = email_error
                    raise forms.ValidationError(email_error)

            return email.lower()

        def clean_password(self):
            password = self.cleaned_data.get('password')
            if password:
                if not len(password) >= 8:
                    password_error = _("Passwords must contain at least 8 letters.")
                    self.cleaned_data['register_password_error'] = password_error
                    raise forms.ValidationError(password_error)
            return password

    permission = None
    form_class = RegisterForm

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(CreateAccountView, self).dispatch(*args, **kwargs)

    def form_invalid(self, form):
        errors = []
        register_email_error = form.cleaned_data.get('register_email_error', None)
        register_password_error = form.cleaned_data.get('register_password_error', None)
        password_error = form.cleaned_data.get('password_error', None)

        if password_error:
            errors.append(password_error)
        if register_email_error:
            errors.append(register_email_error)
        if register_password_error:
            errors.append(register_password_error)

        return JsonResponse(dict(errors=errors), safe=False)

    def form_valid(self, form):
        # create our user
        username = self.form.cleaned_data['email']
        user = Org.create_user(username, self.form.cleaned_data['password'])

        user.first_name = self.form.cleaned_data['first_name']
        user.last_name = self.form.cleaned_data['last_name']
        user.is_active = False
        user.save()

        # TODO Here would be the push notification to Admin

        # log the user in
        user = authenticate(username=user.username, password=self.form.cleaned_data['password'])
        login(self.request, user)

        org = self.form.cleaned_data['org']
        org.surveyors.add(user)

        surveyors_group = Group.objects.get(name="Surveyors")
        token = APIToken.get_or_create(org, user, role=surveyors_group)
        return JsonResponse(dict(token=token.key, user=dict(first_name=user.first_name,
                                 last_name=user.last_name), org=dict(id=org.id, name=org.name)), safe=False)