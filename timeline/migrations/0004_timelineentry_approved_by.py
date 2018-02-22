# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-13 09:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('timeline', '0003_auto_20180211_1924'),
    ]

    operations = [
        migrations.AddField(
            model_name='timelineentry',
            name='approved_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
