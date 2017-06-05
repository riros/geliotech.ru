# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-04 13:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import www.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Catalog',
            fields=[
                ('alias', models.CharField(help_text='Каталог товара', max_length=60, primary_key=True, serialize=False, verbose_name='Каталог товара')),
                ('desc', models.CharField(max_length=50, verbose_name='Читаемое название каталога')),
                ('active', models.BooleanField(default=True, verbose_name='Показывать')),
                ('imported', models.BooleanField(default=False, verbose_name='Импортировано')),
            ],
            options={
                'verbose_name_plural': 'Каталог товаров',
                'verbose_name': 'Каталог товаров',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Наименование товара')),
                ('desc', models.TextField(verbose_name='Описание')),
                ('source_url', models.URLField(verbose_name='Адрес источника')),
                ('price', models.FloatField(default=0, verbose_name='цена поставщика')),
                ('ampl', models.FloatField(default=1, verbose_name='Множитель наценки')),
                ('active', models.BooleanField(default=True, verbose_name='Показывать')),
                ('imported', models.BooleanField(default=False, verbose_name='Импортировано')),
                ('amount', models.IntegerField(default=1, verbose_name='Доступное количество')),
                ('img_src_href', models.URLField(verbose_name='Ссылка на оригинал изображения')),
                ('img', models.ImageField(upload_to=www.models.dynamic_path, verbose_name='Изобраение')),
                ('cat', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='www.Catalog')),
            ],
            options={
                'verbose_name_plural': 'Товар',
                'verbose_name': 'Товар',
            },
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]