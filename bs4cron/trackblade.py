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
from Shopist.models import Post, UserModel
from django.core.mail import send_mail
# Create your views here.
listsitem = []
objects = UserModel.objects.all()
for obj in objects:
    if 'HM' == obj.site:
        hm = requests.get(obj.url)
        sourcehm = BeautifulSoup(hm.content, "lxml")
        newhm = sourcehm.find('span',class_="price-value")
        if newhm:
            newhmr = sourcehm.find('span',class_="price-value").get_text().strip().replace('TL','').replace(',', '').replace('.', '')
            pricedisplay = sourcehm.find('span',class_="price-value").get_text().strip()
        else:
            newhmr = "0"
            pricedisplay = "0"
        listsitem.append({
            'isim' :obj.title,
            'track': newhmr,
            'url': obj.url,
            'image': obj.imageurl,
            'user': obj.user,
            'no':obj.no,
            'site':obj.site,
            'pricedisplay': pricedisplay,
            'serinotrack': obj.serino,
            'email': obj.email,
            })
    if 'Trendyol' == obj.site:
        tr = requests.get(obj.url, allow_redirects=False)
        sourcetr = BeautifulSoup(tr.content, "lxml")
        newtr = sourcetr.find(class_="sale-price")
        if newtr:
            newtr = sourcetr.find(class_="sale-price").get_text().strip().replace('TL', '').replace(',', '').replace('.', '')
            pricedisplay = sourcetr.find(class_="sale-price").get_text().strip()
        else:
            newtr = "0"
            pricedisplay = "0"
        listsitem.append({
            'isim' :obj.title,
            'track': newtr,
            'url': obj.url,
            'image': obj.imageurl,
            'user': obj.user,
            'no':obj.no,
            'site':obj.site,
            'pricedisplay': pricedisplay,
            'serinotrack': obj.serino,
            'email': obj.email,
            })
    if 'Boyner' == obj.site:
        rbs = requests.get(obj.url)
        sourceboyners = BeautifulSoup(rbs.content, "lxml")
        newbrs = sourceboyners.find(class_='price-item')
        if newbrs:
            newbrsr = newbrs.find('ins').get_text().strip().replace('TL','').replace(',', '').replace('.', '')
            pricedisplay = newbrs.find('ins').get_text().strip()
        else:
            newbrsr = "0"
            pricedisplay = "0"
        listsitem.append({
            'isim' :obj.title,
            'track': newbrsr,
            'url': obj.url,
            'image': obj.imageurl,
            'user': obj.user,
            'no':obj.no,
            'site':obj.site,
            'pricedisplay': pricedisplay,
            'serinotrack': obj.serino,
            'email': obj.email,
            })
    if 'Morhipo' == obj.site:
        mrpobj = requests.get(obj.url, allow_redirects=False)
        sourcemrpobj = BeautifulSoup(mrpobj.content, "lxml")
        newmrp = sourcemrpobj.find(class_="final-price text-danger")
        if newmrp:
            newmrpr = newmrp.find('strong').get_text().strip().replace('TL','').replace(',', '').replace('.', '')
            pricedisplay = newmrp.find('strong').get_text().strip()
        else:
            newmrpr = "0"
            pricedisplay = "0"
        listsitem.append({
            'isim': obj.title,
            'track': newmrpr,
            'url': obj.url,
            'image': obj.imageurl,
            'user': obj.user,
            'no': obj.no,
            'site': obj.site,
            'pricedisplay': pricedisplay,
            'serinotrack': obj.serino,
            'email': obj.email,
            })
    if 'Markafoni' == obj.site:
        mrkfobj = requests.get(obj.url, allow_redirects=False)
        sourcemrkfobjobj = BeautifulSoup(mrkfobj.content, "lxml")
        newmrkfobj = sourcemrkfobjobj.find(class_='display-inline-block', attrs={'data-pro-product-info':'sale_price'})
        if newmrkfobj:
            newmrkfobjs = sourcemrkfobjobj.find(class_='display-inline-block', attrs={'data-pro-product-info':'sale_price'}).get_text()\
                .strip().replace('TL', '').replace(',', '').replace('.', '')
            pricedisplay = sourcemrkfobjobj.find(class_='display-inline-block', attrs={'data-pro-product-info':'sale_price'}).get_text().strip()
        else:
            newmrkfobjs = "0"
            pricedisplay = "0"
        listsitem.append({
            'isim': obj.title,
            'track': newmrkfobjs,
            'url': obj.url,
            'image': obj.imageurl,
            'user': obj.user,
            'no': obj.no,
            'site': obj.site,
            'pricedisplay': pricedisplay,
            'serinotrack': obj.serino,
            'email': obj.email,
            })
    if 'ipekyol' == obj.site:
        ipknm = requests.get(obj.url, allow_redirects=False)
        rhmi = BeautifulSoup(ipknm.content, "lxml")
        newsourcehmi = rhmi.find(class_='priceleftt')
        if newsourcehmi:
            newsourcehmi = rhmi.find('div', class_="priceleftt").get_text().strip()[0:8].replace('\r\n', '').replace(
                                    ',', '').replace('.', '')
            pricedisplay = rhmi.find('div', class_="pricebox").get_text().strip()[0:8].replace('\r\n','')
        else:
            newsourcehmi = "0"
            pricedisplay = "0"
        listsitem.append({
            'isim': obj.title,
            'track': newsourcehmi,
            'url': obj.url,
            'image': obj.imageurl,
            'user': obj.user,
            'no': obj.no,
            'site': obj.site,
            'pricedisplay': pricedisplay,
            'serinotrack': obj.serino,
            'email': obj.email,
            })
    if 'Network' == obj.site:
        mrkfobj = requests.get(obj.url, allow_redirects=False)
        sourcemrkfobjobj = BeautifulSoup(mrkfobj.content, "lxml")
        newmrkfobj = sourcemrkfobjobj.find('small', class_="actualPrice")
        if newmrkfobj:
            newmrkfobjs = sourcemrkfobjobj.find('small', class_="actualPrice").get_text()\
                .strip().replace('TL', '').replace(',', '').replace('.', '')
            pricedisplay = sourcemrkfobjobj.find('small', class_="actualPrice").get_text().strip()
        else:
            newmrkfobjs = "0"
            pricedisplay = "0"
        listsitem.append({
            'isim': obj.title,
            'track': newmrkfobjs,
            'url': obj.url,
            'image': obj.imageurl,
            'user': obj.user,
            'no': obj.no,
            'site': obj.site,
            'pricedisplay': pricedisplay,
            'serinotrack': obj.serino,
            'email': obj.email,
            })

    if "Nike" == obj.site:
        mrkfobj = requests.get(obj.url, allow_redirects=True)
        sourcemrkfobjobj = BeautifulSoup(mrkfobj.content, "lxml")
        newmrkfobj = sourcemrkfobjobj.find('div', class_="text-color-black")
        if newmrkfobj:
            newmrkfobjs = sourcemrkfobjobj.find('div', class_="text-color-black").get_text().strip().replace(' ₺',
                                                                                                         '').replace(
                            ',', '').replace('.', '')
            pricedisplay = sourcemrkfobjobj.find('div', class_="text-color-black").get_text().replace(
                        ' ₺', '').strip()
        else:
            newmrkfobjs = "0"
            pricedisplay = "0"
        listsitem.append({
            'isim': obj.title,
            'track': newmrkfobjs,
            'url': obj.url,
            'image': obj.imageurl,
            'user': obj.user,
            'no': obj.no,
            'site': obj.site,
            'pricedisplay': pricedisplay,
            'serinotrack': obj.serino,
            'email': obj.email,
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
                            pricedisplay=objectitem['pricedisplay'],
                            serinotrack=objectitem['serinotrack'],
                            email=objectitem['email'])
    b.save()

#from django.core.mail import send_mail
#send_mail('sdasdadasd', 'asdasd', 'tugrulv89@foruandme.com', ['tugrulv89@gmail.com'], fail_silently=False)
listsettrack = []
for z in trackitems:
    listsettrack.append(z.serinotrack)
setlists = list(set(listsettrack))

if len(setlists) > 0:
    for item in setlists:
        emaillist = []
        tracks = Post.objects.filter(serinotrack=item).order_by('-crontime')[0:2]
        for comp in tracks:
            emaillist.append([comp.track,[comp.user,comp.isim,comp.serinotrack,comp.track,comp.pricedisplay]])
        if emaillist[0][0] != emaillist[1][0]:
            send_mail("Fiyat Değişikliği" , "Merhaba {0}, {1} {2} ürününün fiyatı {3} TL oldu. Kaçırma!.".format(comp.user,comp.isim,comp.serinotrack,comp.pricedisplay), 'tugrulv89@foruandme.com', ['{0}'.format(comp.email)], fail_silently=False)
            #print("Merhaba {0}, {1} {2} ürününün fiyatı {3} TL oldu. Kaçırma!.".format(comp.user,comp.isim,comp.serinotrack,comp.pricedisplay))
else:
    pass

