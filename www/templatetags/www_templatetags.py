__author__ = 'riros <ivanvalenkov@gmail.com> 02.06.17'
from django import template

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
    return val % k


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
