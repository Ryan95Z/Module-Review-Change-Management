# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-14 12:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(error_messages={'unique': 'This username has already been added to the system'}, max_length=40, unique=True),
        ),
    ]