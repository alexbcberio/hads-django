# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-05-12 21:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20210512_2246'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='num_choices',
            field=models.IntegerField(default=4),
        ),
    ]
