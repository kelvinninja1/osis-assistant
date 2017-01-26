# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-06 16:28
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0087_uuid_not_null'),
    ]

    operations = [
        migrations.AddField(
            model_name='learningunit',
            name='uuid',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, null=True),
        ),
        migrations.AddField(
            model_name='learningunityear',
            name='in_charge',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='learningunityear',
            name='vacant',
            field=models.BooleanField(default=False),
        ),
    ]
