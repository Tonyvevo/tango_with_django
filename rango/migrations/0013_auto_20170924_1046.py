# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-09-24 07:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0012_auto_20170924_1045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
