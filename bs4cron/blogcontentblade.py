import os
import sys

path = '/home/tugrulv89/shopistproject'
if path not in sys.path:
    sys.path.insert(0, path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'shopistproject.settings'
import django

django.setup()
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

import requests
from bs4 import BeautifulSoup
from Shopist.models import ContentBlog
import datetime

sitecontent = []

# atasunoptik mode blog next page 8 gözüküyor.
for i in range(1,2):
    i = str(i)
    atasunurl = requests.get("http://www.atasunoptik.com.tr/blog/category/moda-ve-trend/page/" + i + "/")
    ataxlm = BeautifulSoup(atasunurl.content, "lxml")
    atasuncontent = ataxlm.find_all('div', class_="td-module-thumb")
    for contentata in atasuncontent:
        urlata = contentata.find('a').attrs['href'].replace('//', '')
        ata = requests.get('http://' + urlata)
        atas = BeautifulSoup(ata.content, "lxml")
        atasun = atas.find('div', class_="td-ss-main-content")
        sitecontent.append({
            "title": atasun.find('h1').get_text(),
            "image": "http://" + atasun.find('img').get('src').replace('//', ''),
            "content": atasun.find('p').get_text(),
            "site": "Atasun",
            "slug": ("http://" + urlata).split("/")[-2],
        })

# Pembe Ruj mode blog next page 8 gözüküyor.
for pm in range(1,2):
    pm = str(pm)
    atasunurl = requests.get("http://pemberuj.net/kategori/moda/page/" + pm + "/")
    ataxlm = BeautifulSoup(atasunurl.content, "lxml")
    atacss = ataxlm.find('div', class_="td-ss-main-content")
    atasuncontent = atacss.find_all("h3", class_="entry-title")
    for contentata in atasuncontent:
        urlata = contentata.find('a').attrs['href']
        ata = requests.get(urlata)
        atas = BeautifulSoup(ata.content, "lxml")
        atasun = atas.find('div', class_="td-ss-main-content")
        sitecontent.append({
            "title": atasun.find('h1', class_="entry-title").get_text(),
            "image": atasun.find('img').get('src'),
            "content": atasun.find('div', class_="td-post-content").get_text().strip(),
            "site": "Pembe Ruj",
            "slug": urlata.split("/")[-2],
        })

for pm in range(1,2):
    pm = str(pm)
    atasunurl = requests.get("http://blog.sateen.com/page/" + pm + "/")
    ataxlm = BeautifulSoup(atasunurl.content, "lxml")
    atacss = ataxlm.find('div', class_="content content-home")
    atasuncontent = atacss.find_all("h2", class_="title entry-title")
    for contentata in atasuncontent:
        urlata = contentata.find('a').attrs['href']
        ata = requests.get(urlata)
        atas = BeautifulSoup(ata.content, "lxml")
        atasun = atas.find('div', class_="content")
        sitecontent.append({
            "title": atasun.find('h1', class_="title entry-title").get_text(),
            "image": atasun.find('img', class_="attachment-featured size-featured wp-post-image").get('src'),
            "content": atasun.find('div', class_="post-content entry-content single-post-content").get_text().strip(),
            "site": "saaten",
            "slug": (urlata.split("/")[-2]).split(".")[0],
        })





for objectitem in sitecontent:
    cfa = ContentBlog(title=objectitem['title'],
               image=objectitem['image'],
               content=objectitem['content'],
               site=objectitem['site'],
                      slug=objectitem['slug'])
    cfa.save()

