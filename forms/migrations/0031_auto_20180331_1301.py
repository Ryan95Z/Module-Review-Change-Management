# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-31 12:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0030_auto_20180331_1300'),
    ]

    operations = [
        migrations.RenameField(
            model_name='moduleassessment',
            old_name='copy_version',
            new_name='copy_number',
        ),
        migrations.RenameField(
            model_name='modulereassessment',
            old_name='copy_version',
            new_name='copy_number',
        ),
        migrations.RenameField(
            model_name='modulesoftware',
            old_name='copy_version',
            new_name='copy_number',
        ),
        migrations.RenameField(
            model_name='modulesupport',
            old_name='copy_version',
            new_name='copy_number',
        ),
        migrations.RenameField(
            model_name='moduleteaching',
            old_name='copy_version',
            new_name='copy_number',
        ),
    ]
