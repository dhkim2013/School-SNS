# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-19 14:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_auto_20161119_2303'),
    ]

    operations = [
        migrations.AlterField(
            model_name='custumuser',
            name='profileImage',
            field=models.ImageField(default='/profiles/default.jpg', upload_to='/profiles/'),
        ),
    ]
