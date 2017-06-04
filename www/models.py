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
        verbose_name = 'Каталог товаров'
        verbose_name_plural = 'Каталог товаров'


class Product(Model):
    @staticmethod
    def dynamic_path(inst, filename):
        name, ext = path.splitext(filename)
        return 'products/%s/%s%s' % (inst.cat.alias, md5(filename.encode()).hexdigest(), ext)

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

    img = ImageField(verbose_name='Изобраение',
                     upload_to=dynamic_path
                     )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товар'


class Test(Model):
    pass
