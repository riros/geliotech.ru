from django.shortcuts import render
from django.conf import settings
from www.models import Catalog, Product

# Create your views here.

def index(request):
    return page(request, 'index')


def page(request, page):
    return render(request, page + '.html',
                  context={
                      "DEBUG": settings.DEBUG,
                      'breadcrums': False,
                      'menu': [
                          {'path': '/',
                           'name': 'Главная',
                           'active': True
                           },
                          {"path": 'catalog',
                           'name': 'Продукция',
                           'submenu': [{'path': cat.alias, 'name': cat.desc} for cat in Catalog.objects.all()]
                           }
                          , {'path': '/ysolar.html',
                             'name': 'ЯSolar'}
                      ]
                  })


def catalog(r, catalog_alias):
    catalog = Catalog.objects.get(alias=catalog_alias, active=True)
    products = Product.objects.filter(cat=catalog_alias, active=True)
    breadcrums = [{'/': "главная"}, {catalog_alias: catalog.desc}]
    return render(r, 'catalog.html',
                  context={
                      "DEBUG": settings.DEBUG,
                      'breadcrums': breadcrums,
                      'products': products,
                      'catalog': catalog,
                      'menu': [
                          {'path': '/',
                           'name': 'Главная'
                           },
                          {"path": 'catalog',
                           'name': 'Продукция',
                           'submenu': [{'path': cat.alias, 'name': cat.desc} for cat in Catalog.objects.all()],
                           'active': True
                           }
                          , {'path': '/ysolar.html',
                             'name': 'ЯSolar'}
                      ]
                  }
                  )


def product(r, catalog_alias, id):
    catalog = Catalog.objects.get(alias=catalog_alias)
    product = Product.objects.get(id=id)
    breadcrums = [{'/': "главная"},
                  {catalog_alias: catalog.desc}, {'#': product.name}
                  ]
    return render(r, 'product.html',
                  context={
                      "DEBUG": settings.DEBUG,
                      'breadcrums': breadcrums,
                      'product': product,
                      'menu': [
                          {'path': '/',
                           'name': 'Главная'
                           },
                          {"path": 'catalog',
                           'name': 'Продукция',
                           'submenu': [{'path': cat.alias, 'name': cat.desc} for cat in Catalog.objects.all()],
                           'active': True
                           },
                          {'path': '/ysolar.html',
                           'name': 'ЯSolar',
                           }
                      ]
                  }
                  )
