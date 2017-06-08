from django.db import models
from django.db.models \
    import CharField, UUIDField, Model, \
    IntegerField, TextField, FloatField, DateField, BooleanField, ManyToOneRel, URLField, ForeignKey, ImageField

from os import path
from hashlib import md5
from django.utils.html import format_html


# Create your models here.

class Catalog(Model):
    alias = CharField(max_length=60, primary_key=True, null=False, help_text='Каталог товара',
                      verbose_name='Каталог товара')
    desc = CharField(max_length=50, null=False, verbose_name='Читаемое название каталога')
    active = BooleanField(default=True, verbose_name='Показывать')
    imported = BooleanField(default=False, verbose_name="Импортировано")

    class Meta:
        verbose_name = 'Каталоги товаров'
        verbose_name_plural = 'Каталоги товаров'

    def product_count(self):
        return Product.objects.filter(cat=self.alias).count()

    product_count.short_description = "Кол-во товаров"

    def __str__(self):
        return self.desc


def dynamic_path(inst, fn):
    name, ext = path.splitext(fn)
    return 'products/%s/%s%s' % (inst.cat.alias, md5(fn.encode()).hexdigest(), ext)


# class ProductQuerySet(models.QuerySet):
#     def authors(self):
#         return self.filter()
#
#     def editors(self):
#         return self.filter()
#
#
# class ProductManager(models.Manager):
#     def get_queryset(self):
#         return ProductQuerySet(self.model, using=self._db)
#
#     def authors(self):
#         return self.get_queryset().authors()
#
#     def editors(self):
#         return self.get_queryset().editors()
#     use_for_related_fields = True


class Product(Model):
    name = CharField(max_length=255, null=False, verbose_name='Наименование товара')
    desc = TextField(null=False, verbose_name='Описание')
    source_url = URLField(verbose_name='Адрес источника', null=False)
    price = FloatField(null=False, verbose_name="цена поставщика", default=0)
    ampl = FloatField(verbose_name='Множитель наценки', default=1)
    cat = ForeignKey(Catalog, null=True, verbose_name='Каталог')

    active = BooleanField(default=True, verbose_name='Показывать')
    imported = BooleanField(default=False, verbose_name="Импортировать")
    amount = IntegerField(default=1, null=False, verbose_name="Доступное количество")

    img_src_href = URLField(verbose_name='Ссылка на оригинал изображения', null=False)

    img = ImageField(verbose_name='Изображение',
                     upload_to=dynamic_path
                     )

    # products = ProductManager()

    def __str__(self):
        return self.name

    def img_link(self):
        return format_html(
            '<a href="%s">ссылка</a>' % self.img.url,
        )
    img_link.short_description ="Изображение"

    class Meta:
        verbose_name = 'Товары'
        verbose_name_plural = 'Товары'


class Blog(Model):
    title = CharField(max_length=255, null=False, verbose_name='Заголовок')
    date_add = DateField(auto_now=True, verbose_name='Дата')
    active_from_date = DateField(null=False, verbose_name='Дата активации')
    desc = TextField(verbose_name='Текст новости')
    active = BooleanField(default=True, verbose_name='Активность')
    img = ImageField(verbose_name='Картинка', upload_to='blogs_images')

    class Meta:
        verbose_name = 'Новости'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.title
