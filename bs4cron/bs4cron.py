import requests
import sys
sys.path.append('../lib/python3.6/site-packages/')
from bs4 import BeautifulSoup
from Shopist.models import Post, UserModel
# Create your views here.
listsitem = []
objects = UserModel.objects.all()
for obj in objects:
    if 'HM' == obj.site:
        hm = requests.get(obj.url)
        sourcehm = BeautifulSoup(hm.content, "lxml")
        newhm = sourcehm.find('span',class_="price-value")
        if newhm:
            newhmr = sourcehm.find('span',class_="price-value").get_text().replace('TL','').strip().replace(',', '.')
        else:
            newhmr = "0"
        listsitem.append({
            'isim' :obj.title,
            'track': newhmr,
            'url': obj.url,
            'image': obj.imageurl,
            'user': obj.user,
            'no':obj.no,
            'site':obj.site,
            'pricedisplay': obj.pricedisplay,
            })
    if 'Trendyol' == obj.site:
        tr = requests.get(obj.url)
        sourcetr = BeautifulSoup(tr.content, "lxml")
        newtr = sourcetr.find(class_="sale-price")
        if newtr:
            newtr = sourcetr.find(class_="sale-price").get_text().strip().replace('TL','').replace(',','.')
        else:
            newtr = "0"
        listsitem.append({
            'isim' :obj.title,
            'track': newtr,
            'url': obj.url,
            'image': obj.imageurl,
            'user': obj.user,
            'no':obj.no,
            'site':obj.site,
            'pricedisplay': obj.pricedisplay,
            })
    if 'Boyner' == obj.site:
        rbs = requests.get(obj.url)
        sourceboyners = BeautifulSoup(rbs.content, "lxml")
        newbrs = sourceboyners.find(class_='price-item')
        if newbrs:
            newbrsr = newbrs.find('ins').get_text().strip().replace('TL','').replace(',','.')
        else:
            newbrsr = "0"
        listsitem.append({
            'isim' :obj.title,
            'track': newbrsr,
            'url': obj.url,
            'image': obj.imageurl,
            'user': obj.user,
            'no':obj.no,
            'site':obj.site,
            'pricedisplay': obj.pricedisplay,
            })
    if 'Morhipo' == obj.site:
        mrpobj = requests.get(obj.url)
        sourcemrpobj = BeautifulSoup(mrpobj.content, "lxml")
        newmrp = sourcemrpobj.find(class_="final-price text-danger")
        if newmrp:
            newmrpr = newmrp.find('strong').get_text().strip().replace('TL','').replace(',','.')
        else:
            newmrpr = "0"
        listsitem.append({
            'isim': obj.title,
            'track': newmrpr,
            'url': obj.url,
            'image': obj.imageurl,
            'user': obj.user,
            'no': obj.no,
            'site': obj.site,
            'pricedisplay': obj.pricedisplay,
            })
    if 'Markafoni' == obj.site:
        mrkfobj = requests.get(obj.url)
        sourcemrkfobjobj = BeautifulSoup(mrkfobj.content, "lxml")
        newmrkfobj = sourcemrkfobjobj.find(class_='display-inline-block', attrs={'data-pro-product-info':'sale_price'})
        if newmrkfobj:
            newmrkfobjs = sourcemrkfobjobj.find(class_='display-inline-block', attrs={'data-pro-product-info':'sale_price'}).get_text()\
                .strip().replace('TL', '').replace(',', '.')
        else:
            newmrkfobjs = "0"
        listsitem.append({
            'isim': obj.title,
            'track': newmrkfobjs,
            'url': obj.url,
            'image': obj.imageurl,
            'user': obj.user,
            'no': obj.no,
            'site': obj.site,
            'pricedisplay': obj.pricedisplay,
            })
trackitems = Post.objects.all()

for objectitem in listsitem:

    b = Post(track=objectitem['track'],
             isim=objectitem['isim'],
             url=objectitem['url'],
             image=objectitem['image'],
             user=objectitem['user'],
             no=int(objectitem['no']),
             site=objectitem['site'],
             pricedisplay=objectitem['pricedisplay'])
    b.save()

