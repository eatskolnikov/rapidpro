from __future__ import unicode_literals

from celery.task import task
from temba.utils.queues import nonoverlapping_task
from .models import ExportContactsTask, ContactGroupCount, Contact, ContactGroup


@task(track_started=True, name='export_contacts_task')
def export_contacts_task(id):
    """
    Export contacts to a file and e-mail a link to the user
    """
    ExportContactsTask.objects.get(id=id).perform()


@task(track_started=True, name='export_salesforce_contacts_task')
def export_salesforce_contacts_task(id):
    """
    Export contacts to Salesforce and sends an e-mail to the user when it gets the end.
    """
    ExportContactsTask.objects.get(id=id).perform(event='salesforce')


@nonoverlapping_task(track_started=True, name='squash_contactgroupcounts')
def squash_contactgroupcounts():
    """
    Squashes our ContactGroupCounts into single rows per ContactGroup
    """
    ContactGroupCount.squash()


@task(track_started=True, name='import_salesforce_contacts_task')
def import_salesforce_contacts_task(sf_instance_url, sf_access_token, sf_query, fields, user_id, org_id, counter, contact_group_name):
    """
    Import contacts from Salesforce and sends an e-mail to the user when it gets the end.
    """
    Contact.import_from_salesforce(sf_instance_url, sf_access_token, sf_query, fields, user_id, org_id, counter, contact_group_name)


@task(track_started=True, name='unblock_contacts_task')
def unblock_contacts_task(contact_ids, org_id, groups):
    """
    Unblock contacts
    """
    contacts = Contact.objects.filter(pk__in=contact_ids, org_id=org_id)
    contacts.update(is_blocked=False)

    groups = ContactGroup.user_groups.filter(pk__in=groups).order_by('name')

    if groups:
        for contact in contacts:
            contact.update_static_groups(contact.modified_by, groups)


@task(track_started=True, name="full_release_contact")
def full_release_contact(contact_id):
    contact = Contact.objects.filter(id=contact_id).first()

    if contact and not contact.is_active:
        contact._full_release()
