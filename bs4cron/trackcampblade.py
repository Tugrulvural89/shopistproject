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
from Shopist.models import Post, UserModel, Campaign
from django.core.mail import send_mail
# Create your views here.

homelists = []

trdylfrst = requests.get("https://www.trendyol.com/")
homecontent = BeautifulSoup(trdylfrst.content, "lxml")
hmtry = homecontent.find_all('div', class_="butik large col-lg-12 col-md-12 col-xs-12 ")
for t in hmtry:
    homelists.append({
        "url": "https://www.trendyol.com/" + t.find(class_='butik-img-size').attrs['href'],
        "title": t.find(class_='butik-img-size').attrs['title'],
        "image": t.find(class_='bigBoutiqueImage').get('src'),
        "site": "Trendyol",
    })
mrhipfrst = requests.get("https://www.morhipo.com/kampanya/alisveris")
mrhpfrstcnt = BeautifulSoup(mrhipfrst.content, "lxml")
mrhpfr = mrhpfrstcnt.find_all('div', class_="mh_promotion_container")
for z in mrhpfr[1:5]:
    homelists.append({
        "url": "https://www.morhipo.com" + z.find(class_='campaign-banners').attrs['href'],
        "title": z.find('div', class_='mh_promotion_slogan pull-left').get_text(),
        "image": z.find('img', class_=" lazyloaded"),
        "site": "Morhipo",
    })
neon = requests.get("https://www.n11.com/")
neonfr = BeautifulSoup(neon.content, "lxml")
neonfrt = neonfr.find('div', class_='topMainSlide bannerSlider slider')
xcc = neonfrt.find_all(class_=' center counter-large')
for n in xcc:
    homelists.append({
        "url": n.attrs['href'],
        "title": n.attrs['title'],
        "image": n.find('img').get('src'),
        "site": "N11",
    })

trackitems = Campaign.objects.all()

for objectitem in homelists:

    cd = Campaign(title=objectitem['title'],
             image=objectitem['image'],
             site=objectitem['site'],
             url=objectitem['url'],)
    cd.save()



