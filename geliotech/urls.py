"""ekopanels URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from www.views import index, page, catalog, product, \
    sendmail, news_list, news_item

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
                  url(r'^(?P<page>[\w-]+)\.html/$', page, name='index'),
                  url(r'^catalog/(?P<catalog_alias>[\w-]+)/$', catalog, name='catalog'),
                  url(r'^catalog/(?P<catalog_alias>[\w-]+)/(?P<id>\d+)$', product, name='product'),
                  url(r'^sendmail/$', sendmail),
                  url(r'^news/(?P<id>\d+)$', news_item, name='news_item'),
                  url(r'^news/', news_list, name='news_list'),
                  url(r'^$', index),
                  url(r'^admin/', admin.site.urls),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
