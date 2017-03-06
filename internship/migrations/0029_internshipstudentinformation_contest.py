# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-02 07:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internship', '0028_populate_uuid_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='internshipstudentinformation',
            name='contest',
            field=models.CharField(choices=[('SPECIALIST', 'Specialist'), ('GENERALIST', 'Generalist')], default='GENERALIST', max_length=124),
        ),
    ]
