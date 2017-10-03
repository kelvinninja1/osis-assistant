# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-05 11:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0151_remove_learningunit_description'),
    ]

    operations = [
        migrations.RunSQL("UPDATE base_entity SET country = NULL"),
        migrations.CreateModel(
            name='OfferYearEntity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('external_id', models.CharField(blank=True, max_length=100, null=True)),
                ('changed', models.DateTimeField(auto_now=True, null=True)),
                ('type', models.CharField(blank=True, choices=[('ENTITY_ADMINISTRATION', 'ENTITY_ADMINISTRATION'), ('ENTITY_MANAGEMENT', 'ENTITY_MANAGEMENT')], max_length=30, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='entity',
            name='fax',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='entity',
            name='phone',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='entity',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='reference.Country'),
        ),
        migrations.AddField(
            model_name='offeryearentity',
            name='entity',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Entity'),
        ),
        migrations.AddField(
            model_name='offeryearentity',
            name='offer_year',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.OfferYear'),
        ),
        migrations.AlterUniqueTogether(
            name='offeryearentity',
            unique_together=set([('offer_year', 'type')]),
        ),
    ]