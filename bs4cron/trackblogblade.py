
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
from Shopist.models import Blogs



homepageblog = []
nonbirblog = requests.get("https://blog.n11.com/")
nonbirblogcon = BeautifulSoup(nonbirblog.content, "lxml")
nonbirblogconn = nonbirblogcon.find_all('div', class_="mp-container")[:5]
for blognon in nonbirblogconn:
    homepageblog.append({
        "url": blognon.find(class_='mp-image').attrs['href'],
        "title": blognon.find(class_='mp-title').get_text(),
        "image": blognon.find('img').get('src'),
        "site": "n11",
    })
ggblog = requests.get("https://blog.gittigidiyor.com/")
ggblogcon = BeautifulSoup(ggblog.content, "lxml")
ggblogconn = ggblogcon.find_all('div', class_="box-home")[:5]
for bloggg in ggblogconn:
    homepageblog.append({
        "url": bloggg.find('a').attrs['href'],
        "title": bloggg.find('h3', class_='entry-title').get_text(),
        "image": bloggg.find('img').get('src'),
        "site": "GittiGidiyor",
    })
bynblog = requests.get("http://talks.boyner.com.tr/")
bynrblogcon = BeautifulSoup(bynblog.content, "lxml")
bynrblogconn = bynrblogcon.find_all('div', class_="col-md-3")[:5]
for blogbynr in bynrblogconn:
    homepageblog.append({
        "url": "http://talks.boyner.com.tr" + blogbynr.find('a').attrs['href'],
        "title": blogbynr.find('h2').get_text(),
        "image": "http://talks.boyner.com.tr" + blogbynr.find('img', class_="image-css").get('src'),
        "site": "Boyner",
    })

trackitems = Blogs.objects.all()

for objectitem in homepageblog:

    cf = Blogs(title=objectitem['title'],
                            site=objectitem['site'],
                            url=objectitem['url'],
                            image=objectitem['image'])
    cf.save()