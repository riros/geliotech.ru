from django.contrib import admin

# Register your models here.

from www.models import Blog, Catalog, Product


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    pass


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):
    pass


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


admin.autodiscover()
