# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-15 18:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0015_auto_20180315_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moduledescriptionentry',
            name='boolean_entry',
            field=models.NullBooleanField(),
        ),
    ]
