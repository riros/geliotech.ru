# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-07 11:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0003_auto_20170606_2121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='cat',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='www.Catalog', verbose_name='Каталог'),
        ),
    ]
