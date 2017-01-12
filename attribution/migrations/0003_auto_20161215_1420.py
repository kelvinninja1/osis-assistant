# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-15 13:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0083_auto_20161215_1414'),
        ('attribution', '0002_move_data_from_base_attribution_to_attribution_attribution'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttributionCharge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True)),
                ('allocation_charge', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='attribution',
            name='function',
            field=models.CharField(blank=True, choices=[('COORDINATOR', 'COORDINATOR'), ('HOLDER', 'HOLDER'), ('CO_HOLDER', 'CO_HOLDER'), ('DEPUTY', 'DEPUTY'), ('PROFESSOR', 'PROFESSOR')], db_index=True, max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='attributioncharge',
            name='attribution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attribution.Attribution'),
        ),
        migrations.AddField(
            model_name='attributioncharge',
            name='learning_unit_component',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.LearningUnitComponent'),
        ),
    ]