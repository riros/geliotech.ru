# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-06 18:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0002_auto_20170606_2121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='active_from_date',
            field=models.DateField(verbose_name='Дата активации'),
        ),
    ]
