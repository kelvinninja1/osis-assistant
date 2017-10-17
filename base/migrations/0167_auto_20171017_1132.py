# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-17 09:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0166_educationgrouporganization'),
    ]

    operations = [
        migrations.AddField(
            model_name='campus',
            name='code',
            field=models.CharField(blank=True, max_length=1, null=True),
        ),
        migrations.AddField(
            model_name='campus',
            name='is_administration',
            field=models.BooleanField(default=False),
        ),
    ]
