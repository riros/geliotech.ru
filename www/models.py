from django.db.models \
    import CharField, UUIDField, Model, \
    IntegerField, TextField, FloatField, DateField, BooleanField, ManyToOneRel, URLField, ForeignKey, ImageField

from os import path
from hashlib import md5


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


def dynamic_path(inst, fn):
    name, ext =  path.splitext(fn)
    return 'products/%s/%s%s' % (inst.cat.alias, md5(fn.encode()).hexdigest(), ext)


class Product(Model):
    name = CharField(max_length=255, null=False, verbose_name='Наименование товара')
    desc = TextField(null=False, verbose_name='Описание')
    source_url = URLField(verbose_name='Адрес источника', null=False)
    price = FloatField(null=False, verbose_name="цена поставщика", default=0)
    ampl = FloatField(verbose_name='Множитель наценки', default=1)
    cat = ForeignKey(Catalog, null=True)

    active = BooleanField(default=True, verbose_name='Показывать')
    imported = BooleanField(default=False, verbose_name="Импортировано")
    amount = IntegerField(default=1, null=False, verbose_name="Доступное количество")

    img_src_href = URLField(verbose_name='Ссылка на оригинал изображения', null=False)

    img = ImageField(verbose_name='Изображение',
                     upload_to=dynamic_path
                     )

    class Meta:
        verbose_name = 'Товары'
        verbose_name_plural = 'Товары'


class Blog(Model):
    title = CharField(max_length=255, null=False, verbose_name='Заголовок')
    date = DateField(auto_now=True, verbose_name='Дата')
    desc = TextField(verbose_name='Текст новости')
    active = BooleanField(default=True, verbose_name='Активность')
    img = ImageField(verbose_name='Картинка', upload_to='blogs_images')

    class Meta:
        verbose_name = 'Новости'
        verbose_name_plural = 'Новости'