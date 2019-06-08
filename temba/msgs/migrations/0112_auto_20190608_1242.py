# Generated by Django 2.1.5 on 2019-06-08 15:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('msgs', '0111_auto_20171116_0922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='broadcast',
            name='channel',
            field=models.ForeignKey(help_text='Channel to use for message sending', null=True, on_delete=django.db.models.deletion.PROTECT, to='channels.Channel', verbose_name='Channel'),
        ),
        migrations.AlterField(
            model_name='broadcast',
            name='created_by',
            field=models.ForeignKey(help_text='The user which originally created this item', on_delete=django.db.models.deletion.PROTECT, related_name='msgs_broadcast_creations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='broadcast',
            name='modified_by',
            field=models.ForeignKey(help_text='The user which last modified this item', on_delete=django.db.models.deletion.PROTECT, related_name='msgs_broadcast_modifications', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='broadcast',
            name='org',
            field=models.ForeignKey(help_text='The org this broadcast is connected to', on_delete=django.db.models.deletion.PROTECT, to='orgs.Org', verbose_name='Org'),
        ),
        migrations.AlterField(
            model_name='broadcast',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='msgs.Broadcast', verbose_name='Parent'),
        ),
        migrations.AlterField(
            model_name='broadcast',
            name='schedule',
            field=models.OneToOneField(help_text='Our recurring schedule if we have one', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='broadcast', to='schedules.Schedule', verbose_name='Schedule'),
        ),
        migrations.AlterField(
            model_name='broadcastrecipient',
            name='broadcast',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='msgs.Broadcast'),
        ),
        migrations.AlterField(
            model_name='broadcastrecipient',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='contacts.Contact'),
        ),
        migrations.AlterField(
            model_name='exportmessagestask',
            name='created_by',
            field=models.ForeignKey(help_text='The user which originally created this item', on_delete=django.db.models.deletion.PROTECT, related_name='msgs_exportmessagestask_creations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='exportmessagestask',
            name='label',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='msgs.Label'),
        ),
        migrations.AlterField(
            model_name='exportmessagestask',
            name='modified_by',
            field=models.ForeignKey(help_text='The user which last modified this item', on_delete=django.db.models.deletion.PROTECT, related_name='msgs_exportmessagestask_modifications', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='exportmessagestask',
            name='org',
            field=models.ForeignKey(help_text='The organization of the user.', on_delete=django.db.models.deletion.PROTECT, related_name='exportmessagestasks', to='orgs.Org'),
        ),
        migrations.AlterField(
            model_name='label',
            name='created_by',
            field=models.ForeignKey(help_text='The user which originally created this item', on_delete=django.db.models.deletion.PROTECT, related_name='msgs_label_creations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='label',
            name='folder',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='msgs.Label', verbose_name='Folder'),
        ),
        migrations.AlterField(
            model_name='label',
            name='modified_by',
            field=models.ForeignKey(help_text='The user which last modified this item', on_delete=django.db.models.deletion.PROTECT, related_name='msgs_label_modifications', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='label',
            name='org',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='orgs.Org'),
        ),
        migrations.AlterField(
            model_name='labelcount',
            name='label',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='counts', to='msgs.Label'),
        ),
        migrations.AlterField(
            model_name='msg',
            name='broadcast',
            field=models.ForeignKey(blank=True, help_text='If this message was sent to more than one recipient', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='msgs', to='msgs.Broadcast', verbose_name='Broadcast'),
        ),
        migrations.AlterField(
            model_name='msg',
            name='channel',
            field=models.ForeignKey(help_text='The channel object that this message is associated with', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='msgs', to='channels.Channel', verbose_name='Channel'),
        ),
        migrations.AlterField(
            model_name='msg',
            name='connection',
            field=models.ForeignKey(help_text='The session this message was a part of if any', null=True, on_delete=django.db.models.deletion.PROTECT, to='channels.ChannelSession'),
        ),
        migrations.AlterField(
            model_name='msg',
            name='contact',
            field=models.ForeignKey(db_index=False, help_text='The contact this message is communicating with', on_delete=django.db.models.deletion.PROTECT, related_name='msgs', to='contacts.Contact', verbose_name='Contact'),
        ),
        migrations.AlterField(
            model_name='msg',
            name='contact_urn',
            field=models.ForeignKey(help_text='The URN this message is communicating with', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='msgs', to='contacts.ContactURN', verbose_name='Contact URN'),
        ),
        migrations.AlterField(
            model_name='msg',
            name='org',
            field=models.ForeignKey(help_text='The org this message is connected to', on_delete=django.db.models.deletion.PROTECT, related_name='msgs', to='orgs.Org', verbose_name='Org'),
        ),
        migrations.AlterField(
            model_name='msg',
            name='response_to',
            field=models.ForeignKey(blank=True, db_index=False, help_text='The message that this message is in reply to', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='responses', to='msgs.Msg', verbose_name='Response To'),
        ),
        migrations.AlterField(
            model_name='systemlabelcount',
            name='org',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='system_labels', to='orgs.Org'),
        ),
    ]
