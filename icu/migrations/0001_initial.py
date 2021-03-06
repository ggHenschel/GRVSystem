# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-18 20:55
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('mac_address', models.TextField(primary_key=True, serialize=False, unique=True)),
                ('ip_address', models.GenericIPAddressField(unique=True)),
                ('device_name', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='DeviceModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_model', models.TextField(max_length=120)),
            ],
        ),
        migrations.CreateModel(
            name='DeviceType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_name', models.TextField(max_length=50)),
                ('type_description', models.TextField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.TextField(max_length=30)),
                ('last_name', models.TextField(max_length=80)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.TextField(max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='devicemodel',
            name='device_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='icu.DeviceType'),
        ),
        migrations.AddField(
            model_name='device',
            name='device_model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='icu.DeviceModel'),
        ),
    ]
