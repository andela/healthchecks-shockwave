# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-22 14:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_profile_current_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='priority',
            field=models.IntegerField(default=0),
        ),
    ]
