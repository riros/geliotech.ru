__author__ = 'riros <ivanvalenkov@gmail.com> 16.02.17'
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist

import bs4
import requests as req
import re

from www.models import Catalog, Product
import urllib3, urllib.parse

from django.core.files.base import ContentFile
from django.conf import settings
import os


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
                return False
            return ret

        site = settings.SRC_SITE
        cat_links = {}
        items = []
        page = req.get(os.path.join(site, 'catalog'))
        lvl1 = bs4.BeautifulSoup(page.text, 'html.parser')
        soup_cats = lvl1.find("ul", class_="styled")
        lis = soup_cats.find_all('li')
        for li in lis:
            if len(li.a['href']):
                cat_links.update({li.a['href'].replace('/', ''): li.a.text})

        for cat_alias, hr_name in cat_links.items():
            catalog, created = Catalog.objects.get_or_create(alias=cat_alias)
            if catalog.imported:
                catalog.desc = hr_name
                catalog.alias = cat_alias
                catalog.imported = True
                catalog.save()

            soup_items = bs4.BeautifulSoup(req.get(os.path.join(site, cat_alias)).text, 'html.parser') \
                .find_all('div', class_='service-item')
            for soup_item in soup_items:
                product_url = os.path.join(settings.SRC_SITE, soup_item.a['href'])
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

                desc = str(tovar.div.find_next_siblings('div', class_='tovartext1')[0])
                desc_soup = bs4.BeautifulSoup(desc, 'html.parser')
                for link in desc_soup.find_all('img'):
                    desc = desc.replace(link.get('src'), os.path.join(settings.SRC_SITE, link.get('src')))
                for link in desc_soup.find_all('a'):
                    desc = desc.replace(link.get('href'), os.path.join(settings.SRC_SITE, link.get('href')))

                item = {
                    'source_url': product_url,
                    'image_thumb': os.path.join(settings.SRC_SITE, soup_item.a.img['src']),
                    'img_src_href': os.path.join(settings.SRC_SITE, tovar.div.img['src']),
                    'price': price,
                    'catalog': cat_alias,
                    'catalog_hr': hr_name,
                    'name': soup_item.a.h4.text,
                    'desc': desc
                }
                items.append(item)

                product, created = Product.objects.get_or_create(
                    name=item['name'],
                )

                if product.imported:
                    product.cat = Catalog.objects.get(alias=item['catalog'])
                    product.name = item['name']
                    product.desc = item['desc']
                    product.source_url = item['source_url']

                    if filecontent:
                        product.img_src_href = item['img_src_href']
                        if not created:
                            product.img.delete(False)
                        product.img.save(item['img_src_href'], filecontent)
                    else:
                        filecontent = retrieve_image(settings.SRC_SITE, "images/tovar/gvs/unnamed.png")
                        tovar.img.save("images/tovar/gvs/unnamed.png", filecontent)
                        print("Error url: %s" % (settings.SRC_SITE + item['img_src_href']))

                    product.price = item['price']
                    product.save()
