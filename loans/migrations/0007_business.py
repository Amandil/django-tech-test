# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-06 19:02
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0006_auto_20170506_1706'),
    ]

    operations = [
        migrations.CreateModel(
            name='Business',
            fields=[
                ('rcn', models.PositiveIntegerField(primary_key=True, serialize=False, unique=True, validators=[django.core.validators.MaxValueValidator(99999999)])),
                ('name', models.CharField(max_length=60)),
                ('sector', models.CharField(choices=[('RT', 'Retail'), ('PS', 'Professional Services'), ('FD', 'Food & Drink'), ('EN', 'Entertainment')], max_length=2)),
                ('address_one', models.CharField(max_length=255)),
                ('address_two', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('postcode', models.CharField(max_length=10)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='loans.Borrower')),
            ],
        ),
    ]