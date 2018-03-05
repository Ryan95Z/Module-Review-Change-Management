# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-08 18:23
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0015_merge_20180208_1242'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModuleExam',
            fields=[
                ('exam_id', models.AutoField(primary_key=True, serialize=False)),
                ('exam_duration', models.PositiveSmallIntegerField()),
                ('exam_weight', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(100)])),
                ('exam_semester', models.CharField(choices=[('Autumn Semester', 'Autumn Semester'), ('Spring Semester', 'Spring Semester')], max_length=15)),
                ('module_code', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.Module')),
            ],
        ),
        migrations.CreateModel(
            name='ModuleSoftware',
            fields=[
                ('software_id', models.AutoField(primary_key=True, serialize=False)),
                ('software_name', models.CharField(max_length=50)),
                ('software_version', models.CharField(blank=True, max_length=10)),
                ('software_packages', models.CharField(blank=True, max_length=100)),
                ('software_tags', models.CharField(blank=True, max_length=100)),
                ('software_additional_comment', models.TextField(blank=True, max_length=500)),
                ('module_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Module')),
            ],
        ),
        migrations.CreateModel(
            name='ModuleSupport',
            fields=[
                ('support_id', models.AutoField(primary_key=True, serialize=False)),
                ('lab_support_required', models.BooleanField(default=False)),
                ('lab_support_skills', models.CharField(blank=True, max_length=500)),
                ('lab_support_notes', models.TextField(blank=True, max_length=1000)),
                ('tutorial_support_required', models.BooleanField(default=False)),
                ('tutorial_support_skills', models.CharField(blank=True, max_length=500)),
                ('tutorial_support_notes', models.TextField(blank=True, max_length=1000)),
                ('module_code', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.Module')),
            ],
        ),
        migrations.CreateModel(
            name='ModuleTeaching',
            fields=[
                ('teaching_id', models.AutoField(primary_key=True, serialize=False)),
                ('teaching_lectures', models.PositiveSmallIntegerField(default=0)),
                ('teaching_tutorials', models.PositiveSmallIntegerField(default=0)),
                ('teaching_online', models.PositiveSmallIntegerField(default=0)),
                ('teaching_practical_workshops', models.PositiveSmallIntegerField(default=0)),
                ('teaching_supervised_time', models.PositiveSmallIntegerField(default=0)),
                ('teaching_fieldworks', models.PositiveSmallIntegerField(default=0)),
                ('teaching_external_visits', models.PositiveSmallIntegerField(default=0)),
                ('teaching_schedule_assessment', models.PositiveSmallIntegerField(default=0)),
                ('teaching_placement', models.PositiveSmallIntegerField(default=0)),
                ('module_code', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='core.Module')),
            ],
        ),
    ]
