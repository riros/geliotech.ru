from django.contrib import admin
from django.contrib.admin import StackedInline, TabularInline
from sorl.thumbnail.admin import AdminInlineImageMixin, AdminImageMixin
# Register your models here.

from www.models import Blog, Catalog, Product

from sorl_cropping import ImageCroppingMixin

@admin.register(Blog)
class BlogAdmin(ImageCroppingMixin, admin.ModelAdmin):
    list_display = ('title', 'date_add', 'active_from_date', 'img',)


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    list_display = ('desc', 'alias', 'active', 'imported', 'product_count')
    list_filter = ('imported', 'active')
    list_editable = ('desc', 'imported', 'active')
    list_display_links = ('alias',)


@admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
class ProductAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'ampl', 'cat', 'active', 'imported', 'img_link')
    list_display_links = ('id',)
    list_filter = ('cat', 'imported', 'active',)
    list_editable = ('price', 'ampl', 'cat', 'active', 'imported')
    search_fields = ('price', 'ampl', 'name')
    list_per_page = 10
    ordering = ['id']


admin.site.site_header = 'Geliotech.ru'
admin.site.site_title = 'Администрирование'
admin.site.index_title = 'Начало'
