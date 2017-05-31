__author__ = 'riros <ivanvalenkov@gmail.com> 16.02.17'
from django.core.management.base import BaseCommand, CommandError

from django.db import transaction
import os, json, uuid
import datetime
import transliterate
import bs4
import json
import requests as req
import re


class Command(BaseCommand):
    help = "TODO"

    # def add_arguments(self, parser):
    #     parser.add_argument('files', nargs='+', type=str)

    def handle(self, *args, **options):

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
            cat_url = site + '/' + cat_name
            page_lvl2 = req.get(cat_url)
            soup_lvl2 = bs4.BeautifulSoup(page_lvl2.text, 'html.parser')

            soup_items = soup_lvl2.find_all('div', class_='service-item')
            for item in soup_items:
                product_url = site + '/' + item.a['href']
                page_lvl3 = req.get(product_url)
                soup_lvl3 = bs4.BeautifulSoup(page_lvl3.text, 'html.parser')

                tovar = soup_lvl3.find('div', class_='tovar')

                match = re.search('\d+', tovar.div.h4.text)
                price = match.group(0) if match else 0

                items.append({
                    'url': product_url,
                    'image_thumb': site + '/' + item.a.img['src'],
                    'image_href': tovar.div.img['src'],
                    'price': price,
                    'catalog': cat_name,
                    'catalog_hr': desc,
                    'name': item.a.h4.text,
                    'description': tovar.div.find_next_siblings('div', class_ ='tovartext1')[0].text
                })
                break

        print(json.dumps(items, indent=2, ensure_ascii=False))
