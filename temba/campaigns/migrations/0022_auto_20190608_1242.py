# Generated by Django 2.1.5 on 2019-06-08 15:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('campaigns', '0021_campaignevent_embedded_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='created_by',
            field=models.ForeignKey(help_text='The user which originally created this item', on_delete=django.db.models.deletion.PROTECT, related_name='campaigns_campaign_creations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='group',
            field=models.ForeignKey(help_text='The group this campaign operates on', on_delete=django.db.models.deletion.PROTECT, to='contacts.ContactGroup'),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='modified_by',
            field=models.ForeignKey(help_text='The user which last modified this item', on_delete=django.db.models.deletion.PROTECT, related_name='campaigns_campaign_modifications', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='campaign',
            name='org',
            field=models.ForeignKey(help_text='The organization this campaign exists for', on_delete=django.db.models.deletion.PROTECT, to='orgs.Org'),
        ),
        migrations.AlterField(
            model_name='campaignevent',
            name='campaign',
            field=models.ForeignKey(help_text='The campaign this event is part of', on_delete=django.db.models.deletion.PROTECT, related_name='events', to='campaigns.Campaign'),
        ),
        migrations.AlterField(
            model_name='campaignevent',
            name='created_by',
            field=models.ForeignKey(help_text='The user which originally created this item', on_delete=django.db.models.deletion.PROTECT, related_name='campaigns_campaignevent_creations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='campaignevent',
            name='flow',
            field=models.ForeignKey(help_text='The flow that will be triggered', on_delete=django.db.models.deletion.PROTECT, related_name='events', to='flows.Flow'),
        ),
        migrations.AlterField(
            model_name='campaignevent',
            name='modified_by',
            field=models.ForeignKey(help_text='The user which last modified this item', on_delete=django.db.models.deletion.PROTECT, related_name='campaigns_campaignevent_modifications', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='campaignevent',
            name='relative_to',
            field=models.ForeignKey(help_text='The field our offset is relative to', on_delete=django.db.models.deletion.PROTECT, related_name='campaigns', to='contacts.ContactField'),
        ),
        migrations.AlterField(
            model_name='eventfire',
            name='contact',
            field=models.ForeignKey(help_text='The contact that is scheduled to have an event run', on_delete=django.db.models.deletion.PROTECT, related_name='fire_events', to='contacts.Contact'),
        ),
        migrations.AlterField(
            model_name='eventfire',
            name='event',
            field=models.ForeignKey(help_text='The event that will be fired', on_delete=django.db.models.deletion.PROTECT, related_name='event_fires', to='campaigns.CampaignEvent'),
        ),
    ]