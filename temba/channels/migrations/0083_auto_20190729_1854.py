# Generated by Django 2.1.5 on 2019-07-29 21:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('channels', '0082_auto_20190712_1213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channelcount',
            name='channel',
            field=models.ForeignKey(help_text='The channel this is a daily summary count for', on_delete=django.db.models.deletion.PROTECT, related_name='counts', to='channels.Channel'),
        ),
    ]
