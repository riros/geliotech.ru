from django.contrib import admin

# Register your models here.

from www.models import Blog, Catalog, Product


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_add', 'active_from_date', 'img',)


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ('desc', 'alias', 'active', 'imported', 'product_count')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'ampl', 'cat', 'active', 'imported', 'img' )


admin.site.site_header = 'Geliotech.ru'
admin.site.site_title = 'Администрирование'
admin.site.index_title = 'Начало'