# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-06-01 12:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0276_professional_integration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='learningunit',
            name='end_year',
            field=models.IntegerField(blank=True, null=True, verbose_name='end_year_title'),
        ),
        migrations.AlterField(
            model_name='learningunit',
            name='start_year',
            field=models.IntegerField(verbose_name='start_year'),
        ),
    ]