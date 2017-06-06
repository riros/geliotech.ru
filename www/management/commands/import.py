__author__ = 'riros <ivanvalenkov@gmail.com> 16.02.17'
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist

from django.db import transaction
import os, json, uuid
import datetime
import bs4
import requests as req
import re

from www.models import Catalog, Product
import urllib3, urllib.parse

from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.conf import settings



class Command(BaseCommand):
    help = "TODO"

    # def add_arguments(self, parser):
    #     parser.add_argument('files', nargs='+', type=str)

    def handle(self, *args, **options):

        def retrieve_image(host, url):
            try:
                eurl = urllib.parse.quote_plus(url)
                ret = ContentFile(urllib3.PoolManager().request("GET", host + eurl).data)
            except:
                # TODO Есть ссылки, которые имею символы в странной кодировке, и не подходят для запроса
                return False
            return ret

        site = 'http://ekoproekt-energo.ru'
        cat_links = {}
        items = []
        page = req.get(site + '/catalog/')
        lvl1 = bs4.BeautifulSoup(page.text, 'html.parser')
        soup_cats = lvl1.find("ul", class_="styled")
        lis = soup_cats.find_all('li')
        for li in lis:
            if len(li.a['href']):
                cat_links.update({li.a['href'].replace('/', ''): li.a.text})

        for cat_name, desc in cat_links.items():

            catalog, created = Catalog.objects.get_or_create(alias=cat_name)
            catalog.desc = desc
            catalog.alias = cat_name
            catalog.imported = True
            catalog.save()

            soup_items = bs4.BeautifulSoup(req.get(site + '/' + cat_name).text, 'html.parser') \
                .find_all('div', class_='service-item')
            for soup_item in soup_items:
                product_url = site + '/' + soup_item.a['href']
                try:
                    page_lvl3 = req.get(product_url)
                except:
                    print("Error catch %s" % product_url)
                    break
                soup_lvl3 = bs4.BeautifulSoup(page_lvl3.text, 'html.parser')

                tovar = soup_lvl3.find('div', class_='tovar')

                match = re.search('\d+', tovar.div.h4.text)
                price = match.group(0) if match else 0

                filecontent = retrieve_image(settings.SRC_SITE, tovar.div.img['src'])

                item = {
                    'source_url': product_url,
                    'image_thumb': site + '/' + soup_item.a.img['src'],
                    'img_src_href': tovar.div.img['src'],
                    'price': price,
                    'catalog': cat_name,
                    'catalog_hr': desc,
                    'name': soup_item.a.h4.text,
                    'desc': str(tovar.div.find_next_siblings('div', class_='tovartext1')[0])
                }
                items.append(item)

                tovar, created = Product.objects.get_or_create(
                    name=item['name'],
                )

                tovar.cat = Catalog.objects.get(alias=item['catalog'])
                tovar.name = item['name']
                tovar.desc = item['desc']
                tovar.source_url = item['source_url']

                if filecontent:
                    tovar.img_src_href = item['img_src_href']
                    if not created: tovar.img.delete(False)
                    tovar.img.save(item['img_src_href'], filecontent)
                else:
                    filecontent = retrieve_image(settings.SRC_SITE, "images/tovar/gvs/unnamed.png")
                    tovar.img.save("images/tovar/gvs/unnamed.png", filecontent)
                    print("Error url: %s" % (settings.SRC_SITE + item['img_src_href']))

                tovar.price = item['price']
                tovar.imported = True
                tovar.save()

