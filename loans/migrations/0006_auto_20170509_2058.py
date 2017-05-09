# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-09 20:58
from __future__ import unicode_literals

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0005_auto_20170507_1705'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loan',
            name='loan_deadline',
            field=models.DateField(default=datetime.date.today, validators=[django.core.validators.MinValueValidator(datetime.date(2017, 6, 6)), django.core.validators.MaxValueValidator(datetime.date(2019, 5, 9))]),
        ),
    ]