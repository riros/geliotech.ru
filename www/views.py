from django.shortcuts import render
from django.conf import settings


# Create your views here.

def index(request):
    return render(request, 'index.html', context={
        "DEBUG": settings.DEBUG,
    })


def page(request, page):
    return render(request, page + '.html', context={
        "DEBUG": settings.DEBUG,
    })
