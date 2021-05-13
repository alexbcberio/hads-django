# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-05-13 14:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_question_num_choices'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='is_correct',
        ),
        migrations.AddField(
            model_name='question',
            name='correct_choice',
            field=models.IntegerField(default=1),
        ),
    ]
