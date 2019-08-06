# Generated by Django 2.1.5 on 2019-06-08 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('msgs', '0112_auto_20190608_1242'),
    ]

    operations = [
        migrations.AddField(
            model_name='msg',
            name='delete_reason',
            field=models.CharField(choices=[('A', 'Archive delete'), ('U', 'User delete')], help_text='Why the message is being deleted', max_length=1, null=True),
        ),
    ]