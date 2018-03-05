# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-16 16:41
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forms', '0004_auto_20180215_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moduleassessment',
            name='assessment_duration',
            field=models.PositiveSmallIntegerField(verbose_name='Duration (hours)'),
        ),
        migrations.AlterField(
            model_name='moduleassessment',
            name='assessment_hand_in',
            field=models.CharField(choices=[('1A', 'Autumn Week 1'), ('2A', 'Autumn Week 2'), ('3A', 'Autumn Week 3'), ('4A', 'Autumn Week 4'), ('5A', 'Autumn Week 5'), ('6A', 'Autumn Week 6'), ('7A', 'Autumn Week 7'), ('8A', 'Autumn Week 8'), ('9A', 'Autumn Week 9'), ('10A', 'Autumn Week 10'), ('11A', 'Autumn Week 11'), ('1S', 'Spring Week 1'), ('2S', 'Spring Week 2'), ('3S', 'Spring Week 3'), ('4S', 'Spring Week 4'), ('5S', 'Spring Week 5'), ('6S', 'Spring Week 6'), ('7S', 'Spring Week 7'), ('8S', 'Spring Week 8'), ('9S', 'Spring Week 9'), ('10S', 'Spring Week 10'), ('11S', 'Spring Week 11')], max_length=15, verbose_name='Hand in week'),
        ),
        migrations.AlterField(
            model_name='moduleassessment',
            name='assessment_hand_out',
            field=models.CharField(choices=[('1A', 'Autumn Week 1'), ('2A', 'Autumn Week 2'), ('3A', 'Autumn Week 3'), ('4A', 'Autumn Week 4'), ('5A', 'Autumn Week 5'), ('6A', 'Autumn Week 6'), ('7A', 'Autumn Week 7'), ('8A', 'Autumn Week 8'), ('9A', 'Autumn Week 9'), ('10A', 'Autumn Week 10'), ('11A', 'Autumn Week 11'), ('1S', 'Spring Week 1'), ('2S', 'Spring Week 2'), ('3S', 'Spring Week 3'), ('4S', 'Spring Week 4'), ('5S', 'Spring Week 5'), ('6S', 'Spring Week 6'), ('7S', 'Spring Week 7'), ('8S', 'Spring Week 8'), ('9S', 'Spring Week 9'), ('10S', 'Spring Week 10'), ('11S', 'Spring Week 11')], max_length=15, verbose_name='Hand out week'),
        ),
        migrations.AlterField(
            model_name='moduleassessment',
            name='assessment_semester',
            field=models.CharField(choices=[('Autumn Semester', 'Autumn Semester'), ('Spring Semester', 'Spring Semester')], max_length=15, verbose_name='Semester'),
        ),
        migrations.AlterField(
            model_name='moduleassessment',
            name='assessment_title',
            field=models.CharField(max_length=100, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='moduleassessment',
            name='assessment_type',
            field=models.CharField(max_length=50, verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='moduleassessment',
            name='assessment_weight',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(100)], verbose_name='Weighting'),
        ),
        migrations.AlterField(
            model_name='moduleassessment',
            name='learning_outcomes_covered',
            field=models.CharField(max_length=500, verbose_name='Learning Outcomes Covered'),
        ),
        migrations.AlterField(
            model_name='modulesupport',
            name='lab_support_notes',
            field=models.TextField(blank=True, max_length=1000, verbose_name='Notes'),
        ),
        migrations.AlterField(
            model_name='modulesupport',
            name='lab_support_required',
            field=models.BooleanField(default=False, verbose_name='Do you require PhD student support for your labs?'),
        ),
        migrations.AlterField(
            model_name='modulesupport',
            name='lab_support_skills',
            field=models.CharField(blank=True, max_length=500, verbose_name='What skills will lab tutors require?'),
        ),
        migrations.AlterField(
            model_name='modulesupport',
            name='tutorial_support_notes',
            field=models.TextField(blank=True, max_length=1000, verbose_name='Notes'),
        ),
        migrations.AlterField(
            model_name='modulesupport',
            name='tutorial_support_required',
            field=models.BooleanField(default=False, verbose_name='Do you require Phd student support for your tutorials?'),
        ),
        migrations.AlterField(
            model_name='modulesupport',
            name='tutorial_support_skills',
            field=models.CharField(blank=True, max_length=500, verbose_name='What skills will the tutors require?'),
        ),
    ]
