from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from django.views.generic.base import RedirectView
from rest_framework.urlpatterns import format_suffix_patterns

from .views import AuthenticateView, UserOrgsEndpoint, ContactEndpoint, FlowStepEndpoint, RunsEndpoint, CreateAccountView
from .views import ManageAccountsListEndpoint, ManageAccountsActionEndpoint, DeviceTokenEndpoint
from ..v2.views import BoundariesEndpoint, DefinitionsEndpoint, FieldsEndpoint, FlowsEndpoint, MediaEndpoint, OrgEndpoint


urlpatterns = [
    # this HTML view redirects to its v2 equivalent
    url(r'^explorer/$', RedirectView.as_view(pattern_name='api.v2.explorer', permanent=True)),

    # these endpoints are retained for Android Surveyor clients
    url(r'^$', RedirectView.as_view(pattern_name='api.v2.explorer', permanent=True)),
    url(r'^authenticate$', AuthenticateView.as_view(), name='api.v3.authenticate'),
    url(r'^create-account$', CreateAccountView.as_view(), name='api.v3.create_account'),
    url(r'^user/orgs$', UserOrgsEndpoint.as_view(), name='api.v3.user_orgs'),
    url(r'^user/device-token$', DeviceTokenEndpoint.as_view(), name='api.v3.device_token'),
    url(r'^manage-accounts/list$', ManageAccountsListEndpoint.as_view(), name='api.v3.manage_accounts_list'),
    url(r'^manage-accounts/action/(?P<action>approve|disapprove)$', ManageAccountsActionEndpoint.as_view(), name='api.v3.manage_accounts_action'),

    # Redirect views to v1 and v2
    url(r'^boundaries$', BoundariesEndpoint.as_view(), name='api.v3.boundaries'),
    url(r'^contacts$', ContactEndpoint.as_view(), name='api.v3.contacts'),
    url(r'^definitions$', DefinitionsEndpoint.as_view(), name='api.v3.definitions'),
    url(r'^fields$', FieldsEndpoint.as_view(), name='api.v3.fields'),
    url(r'^flows$', FlowsEndpoint.as_view(), name='api.v3.flows'),
    url(r'^media$', MediaEndpoint.as_view(), name='api.v3.media'),
    url(r'^org$', OrgEndpoint.as_view(), name='api.v3.org'),
    url(r'^steps$', FlowStepEndpoint.as_view(), name='api.v3.steps'),
    url(r'^runs$', RunsEndpoint.as_view(), name='api.v3.runs'),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'api'])