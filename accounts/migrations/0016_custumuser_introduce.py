# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-19 10:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_auto_20161119_1830'),
    ]

    operations = [
        migrations.AddField(
            model_name='custumuser',
            name='introduce',
            field=models.CharField(default='', max_length=100),
        ),
    ]
