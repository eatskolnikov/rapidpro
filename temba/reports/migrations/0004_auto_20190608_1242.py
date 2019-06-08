# Generated by Django 2.1.5 on 2019-06-08 15:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0003_auto_20170228_0837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='created_by',
            field=models.ForeignKey(help_text='The user which originally created this item', on_delete=django.db.models.deletion.PROTECT, related_name='reports_report_creations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='report',
            name='modified_by',
            field=models.ForeignKey(help_text='The user which last modified this item', on_delete=django.db.models.deletion.PROTECT, related_name='reports_report_modifications', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='report',
            name='org',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='orgs.Org'),
        ),
    ]
