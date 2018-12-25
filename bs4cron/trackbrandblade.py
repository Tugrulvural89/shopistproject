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
from Shopist.models import Post, UserModel, Campaign, UrunInput
import datetime

from openpyxl import load_workbook
wb = load_workbook(filename='static/docs/inputt.xlsx', read_only=True)
ws = wb['Sheet1']

urunlists = []
for row in ws.rows:
    for cell in row:
        urunlists.append(cell.value)

sonucurunlists = []

for item in urunlists:
    subjecthm = item
    rhm = requests.get( "https://www2.hm.com/tr_tr/search-results.html?q="+ subjecthm)
    sourcehm = BeautifulSoup(rhm.content, "lxml")
    newsourcehm = sourcehm.find_all('li', attrs={"class": "product-item"})[:6]
    for e in newsourcehm:
        sonucurunlists.append({
            "title": e.find('h3', class_="item-heading").get_text().strip(),
            "price": int
                (e.find('span' ,class_="price").get_text().replace('TL' ,'').strip().replace(',', '').replace('.', '')),
            "pricedisplay": e.find('span', class_="price").get_text().replace('TL', '').strip(),
            "site": "HM",
            "url": "http://www2.hm.com" + e.find(class_="item-link").attrs['href'],
            "serino": e.find(class_="hm-product-item").attrs['data-articlecode'],
            "img": e.find('img', class_="item-image").attrs['data-src'],
            "kelimearama":item,
        })
    subjectboyner = item
    rb = requests.get("https://www.boyner.com.tr/search?searchKey=" + subjectboyner)
    sourceboyner = BeautifulSoup(rb.content, "lxml")
    newboynersource = sourceboyner.find_all('div', attrs={"class" :"product-list-item"})[:6]
    for b in newboynersource:
        sonucurunlists.append({
            "title": b.find(class_="product-name").get_text().strip(),
            "price": int
                (b.find(class_="cs-amount").get_text().strip().replace('TL' ,'').replace(',' ,'').replace('.' ,'')),
            "pricedisplay": b.find(class_="cs-amount").get_text().strip().replace('TL', ''),
            "site": "Boyner",
            "url": "https://www.boyner.com.tr" + b.find(class_="product-figure").attrs['href'],
            "serino": b.find(class_="product-figure").attrs['data-id'],
            "img": b.find('img', class_="lazy").attrs['data-original'],
            "kelimearama":item,
        })

    subjecttrendyol = item
    rt = requests.get \
        ("https://www.trendyol.com/tum--urunler?q=" + subjecttrendyol + "&st=" + subjecttrendyol + " + &qt="  + subjecttrendyol)
    sourcetrendyol = BeautifulSoup(rt.content, "lxml")
    newtrendyolsource = sourcetrendyol.find_all('li', attrs={"class" :"pc-wrp"})[:14]
    for c in newtrendyolsource[0:6]:
        sonucurunlists.append({
            "title": c.find(class_="pname").get_text().strip(),
            "price": int(c.find(class_="prspr").get_text().strip().replace('TL' ,'').replace(',' ,'').replace('.' ,'')),
            "pricedisplay": c.find(class_="prspr").get_text().strip().replace('TL', ''),
            "site": "Trendyol",
            "url": "https://www.trendyol.com/" + c.find(class_="pdlnk").attrs['href'],
            "serino": c.find(class_="favorite").attrs['data-productid'],
            "img": c.find('img', class_="primg").get('src'),
            "kelimearama":item,
        })
    for c in newtrendyolsource[6::]:
        sonucurunlists.append({
            "title": c.find(class_="pname").get_text().strip(),
            "price": int(c.find(class_="prspr").get_text().strip().replace('TL' ,'').replace(',' ,'').replace('.' ,'')),
            "pricedisplay": c.find(class_="prspr").get_text().strip().replace('TL', ''),
            "site": "Trendyol",
            "url": "https://www.trendyol.com/" + c.find(class_="pdlnk").attrs['href'],
            "serino": c.find(class_="favorite").attrs['data-productid'],
            "img": c.find('img', class_="primg lazy").attrs['data-original'],
            "kelimearama":item,
        })
    mrpsrp = item
    mrps = requests.get("https://www.morhipo.com/kampanya/arama?q=" + mrpsrp + "&qcat=ps")
    sourcemrsp = BeautifulSoup(mrps.content, "lxml")
    newmrps = sourcemrsp.find_all('li', class_="col-controlled col-xxs-6 col-xs-6 col-sm-4 col-md-4 col-lg-4 column")[:6]
    for fs in newmrps:
        sonucurunlists.append({
            "title": fs.find('div', class_="brand").get_text(),
            "price": int
                (fs.find(class_="prd_price").get_text().strip().replace('TL' ,'').replace(',' ,'').replace('.' ,'')),
            "pricedisplay": fs.find(class_="prd_price").get_text().strip().replace('TL', ''),
            "site": "Morhipo",
            "url": "https://www.morhipo.com/" + fs.find('a', class_="js-product").attrs['href'],
            "serino": fs.find(class_='enhanced-ecommerce-data').attrs['data-productid'],
            "img": fs.find('img', class_="lazyload").attrs['src'],
            "kelimearama":item,
        })
    mrk = item
    mrks = requests.get("https://www.markafoni.com/arama?q=" + mrk)
    sourcemrk = BeautifulSoup(mrks.content, "lxml")
    newmrk = sourcemrk.find_all(class_="col-xs-4 pro-product-list-item")[:6]
    for mrkfr in newmrk:
        sonucurunlists.append({
            "title": mrkfr.find(class_="pro-product-title -GTM-product-click-action").get_text(),
            "price": int
                (mrkfr.find('div', class_="total-sale-price").attrs['data-sale-price'].strip().replace('TL', '').replace
                    (',' ,'').replace('.', '')),
            "pricedisplay": mrkfr.find('div', class_="total-sale-price").attrs['data-sale-price'].strip().replace('TL', ''),
            "site": "Markafoni",
            "url": "https://www.markafoni.com" + mrkfr.find(class_="pro-product-title -GTM-product-click-action").attrs
                ['href'],
            "serino": mrkfr.find('div', class_='pro-product').attrs['data-gtm-product-id'],
            "img": mrkfr.find('img', class_="visible").attrs['data-original'],
            "kelimearama":item,
        })



for objectitem in sonucurunlists:
    inputu = UrunInput(title=objectitem['title'],
                   price=objectitem['price'],
                   pricedisplay=objectitem['pricedisplay'],
                   site=objectitem['site'],
                   url=objectitem['url'],
                   serino=objectitem['serino'],
                   kelimearama=objectitem['kelimearama'],
                   img=objectitem['img'])
    inputu.save()



trackitems = UrunInput.objects.all().exclude(crontime=datetime.date.today())
trackitems.delete()


