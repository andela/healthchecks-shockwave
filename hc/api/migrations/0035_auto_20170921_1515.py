# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-21 12:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0034_auto_20170921_1513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='check',
            name='priority',
            field=models.CharField(choices=[('up', 'Up'), ('down', 'Down'), ('new', 'New'), ('paused', 'Paused'), ('often', 'Often')], default='Low', max_length=6),
        ),
    ]
