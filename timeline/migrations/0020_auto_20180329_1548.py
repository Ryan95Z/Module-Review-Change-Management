# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-29 14:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timeline', '0019_auto_20180329_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timelineentry',
            name='entry_type',
            field=models.CharField(choices=[('Generic', 'Generic'), ('Tracking-Form', 'Tracking-Form')], default='Generic', max_length=6),
        ),
    ]
