# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-07-11 10:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('dissertation', '0005_auto_20160628_1702'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offerproposition',
            name='day_of_month_end_visibility_dissertation',
        ),
        migrations.RemoveField(
            model_name='offerproposition',
            name='day_of_month_end_visibility_proposition',
        ),
        migrations.RemoveField(
            model_name='offerproposition',
            name='day_of_month_start_visibility_dissertation',
        ),
        migrations.RemoveField(
            model_name='offerproposition',
            name='day_of_month_start_visibility_proposition',
        ),
        migrations.RemoveField(
            model_name='offerproposition',
            name='month_end_visibility_dissertation',
        ),
        migrations.RemoveField(
            model_name='offerproposition',
            name='month_end_visibility_proposition',
        ),
        migrations.RemoveField(
            model_name='offerproposition',
            name='month_start_visibility_dissertation',
        ),
        migrations.RemoveField(
            model_name='offerproposition',
            name='month_start_visibility_proposition',
        ),
        migrations.AddField(
            model_name='offerproposition',
            name='end_visibility_dissertation',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='offerproposition',
            name='end_visibility_proposition',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='offerproposition',
            name='start_visibility_dissertation',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='offerproposition',
            name='start_visibility_proposition',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
