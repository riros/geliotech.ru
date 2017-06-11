__author__ = 'riros <ivanvalenkov@gmail.com> 02.06.17'
from django import template
from django.conf import settings
import bs4

register = template.Library()


@register.filter()
def isdict(val):
    return isinstance(val, dict)


@register.filter()
def islist(val):
    return isinstance(val, list)


@register.filter()
def isactive(val):
    return isinstance(val, dict) and (val['active'])


@register.filter()
def menupath(val):
    return val['path']


@register.filter()
def menuname(val):
    return val['name']


@register.filter()
def submenupresent(val):
    return isinstance(val, dict) and ('submenu' in val)


@register.filter()
def submenu(val):
    return val['submenu']


@register.filter()
def kratnoe(val, k):
    return bool(val % k)


@register.filter()
def nacenka(val, i):
    return int(val * i)


@register.filter()
def key(val):
    for k, v in val.items():
        return k


@register.filter()
def val(val):
    for k, v in val.items():
        return v


@register.filter()
def fixlinks(val):
    import os
    soup = bs4.BeautifulSoup(val, 'html.parser')
    for link in soup.find_all('img'):
        val = val.replace(link.href, os.path.join(settings.SRC_SITE, link.get('src')))
    for link in soup.find_all('a'):
        val = val.replace(link.href, os.path.join(settings.SRC_SITE, link.get('href')))
    return val
