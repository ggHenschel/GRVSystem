# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-30 21:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('icu', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
