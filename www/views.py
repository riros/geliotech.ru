from django.shortcuts import render
from django.conf import settings
from www.models import Catalog, Product, Blog

from django.http import JsonResponse, HttpResponseForbidden

from django.core.mail import send_mail
from datetime import date
import os
from django.views.decorators.cache import cache_page


# Create your views here.
def get_menu():
    menu = [
        {'path': '/',
         'name': 'Главная'
         },
        {"path": '',
         'name': 'Продукция',
         'submenu': [{'path': 'catalog/' + cat.alias, 'name': cat.desc} for cat in
                     Catalog.objects.all()]
         },
        {'path': '/ysolar.html',
         'name': 'ЯSolar'},
        {'path': '/news/',
         'name': 'Новости'},

    ]
    return menu


def activeatemenusection(menu, i):
    for m in menu:
        m['active'] = False
    menu[i]['active'] = True
    return menu


@cache_page(60 * 60 * 24 * 30)
def index(request):
    return page(request, 'index')


@cache_page(60 * 60 * 24 * 30)
def page(request, page):
    if not os.path.exists(os.path.join(settings.BASE_DIR, 'www/templates/' + page + '.html')):
        page = 'index'

    return render(request, page + '.html',
                  context={
                      "DEBUG": settings.DEBUG,
                      'breadcrums': False,
                      'menu': activeatemenusection(get_menu(), 0),
                  })


@cache_page(60 * 60 * 24 * 30)
def catalog(r, catalog_alias):
    catalog = Catalog.objects.get(alias=catalog_alias, active=True)
    products = Product.objects.filter(cat=catalog_alias, active=True)
    breadcrums = [{'#': "главная"}, {'': catalog.desc}]

    return render(r, 'catalog.html',
                  context={
                      "DEBUG": settings.DEBUG,
                      'breadcrums': breadcrums,
                      'products': products,
                      'catalog': catalog,
                      'menu': activeatemenusection(get_menu(), 1)
                  }
                  )


@cache_page(60 * 60 * 24 * 30)
def product(r, catalog_alias, id):
    catalog = Catalog.objects.get(alias=catalog_alias)
    product = Product.objects.get(id=id)
    breadcrums = [{'#': "главная"},
                  {'catalog/' + catalog_alias: catalog.desc}, {'': product.name}
                  ]
    return render(r, 'product.html',
                  context={
                      "DEBUG": settings.DEBUG,
                      'breadcrums': breadcrums,
                      'product': product,
                      'menu': activeatemenusection(get_menu(), 1)
                  }
                  )


@cache_page(60 * 60 * 24 * 30)
def news_list(r):
    blogs = Blog.objects.filter(active=True, active_from_date__lte=date.today())[:6]
    return render(r, 'bloglist.html', context={
        "DEBUG": settings.DEBUG,
        'breadcrums': False,
        'blogs': blogs,
        'menu': activeatemenusection(get_menu(), 3)
    })


@cache_page(60 * 60 * 24 * 30)
def news_item(r, id):
    blog = Blog.objects.get(id=id, active=True, active_from_date__lte=date.today())
    return render(r, 'newsitem.html',
                  context={
                      "DEBUG": settings.DEBUG,
                      'blog': blog,
                      'breadcrums': False,
                      'menu': activeatemenusection(get_menu(), 3)
                  })


def sendmail(request):
    from_name = request.GET.get('name', '')
    phone = request.GET.get('phone', '')
    subject = request.GET.get('admin_email', '')
    message = request.GET.get('Сообщение с geliotech.ru от %s тел %s ' % (from_name, phone), '')
    if phone and from_name:
        send_mail(subject, message, 'riros@ya.ru', ['riros@tbo23.ru'])
    else:
        return HttpResponseForbidden('Случилась ошибка... номер не понятен.')
    return JsonResponse({})
