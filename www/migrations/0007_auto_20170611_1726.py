# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-11 14:26
from __future__ import unicode_literals

from django.db import migrations
import sorl.thumbnail.fields
import www.models


class Migration(migrations.Migration):

    dependencies = [
        ('www', '0006_auto_20170611_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='img',
            field=sorl.thumbnail.fields.ImageField(upload_to='blogs_images', verbose_name='Картинка'),
        ),
        migrations.AlterField(
            model_name='product',
            name='img',
            field=sorl.thumbnail.fields.ImageField(upload_to=www.models.dynamic_path, verbose_name='Изображение'),
        ),
    ]
