# Generated by Django 2.1.5 on 2019-06-08 15:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0009_auto_20170228_0837'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adminboundary',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, help_text='The parent to this political boundary if any', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='children', to='locations.AdminBoundary'),
        ),
        migrations.AlterField(
            model_name='boundaryalias',
            name='boundary',
            field=models.ForeignKey(help_text='The admin boundary this alias applies to', on_delete=django.db.models.deletion.PROTECT, related_name='aliases', to='locations.AdminBoundary'),
        ),
        migrations.AlterField(
            model_name='boundaryalias',
            name='created_by',
            field=models.ForeignKey(help_text='The user which originally created this item', on_delete=django.db.models.deletion.PROTECT, related_name='locations_boundaryalias_creations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='boundaryalias',
            name='modified_by',
            field=models.ForeignKey(help_text='The user which last modified this item', on_delete=django.db.models.deletion.PROTECT, related_name='locations_boundaryalias_modifications', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='boundaryalias',
            name='org',
            field=models.ForeignKey(help_text='The org that owns this alias', on_delete=django.db.models.deletion.PROTECT, to='orgs.Org'),
        ),
    ]
