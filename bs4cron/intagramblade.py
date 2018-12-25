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

import json
import requests
from bs4 import BeautifulSoup
from Shopist.models import Intagram
import datetime

from openpyxl import load_workbook
wb = load_workbook(filename='static/docs/intagraminput.xlsx', read_only=True)
ws = wb['Sheet1']

intagramcontent = []

for row in ws.rows:
    for hastag in row:
        r = requests.get('https://www.instagram.com/explore/tags/' + hastag.value + '/')
        soup = BeautifulSoup(r.text, 'lxml')
        script = soup.find('script', text=lambda t: t.startswith('window._sharedData'))
        page_json = script.text.split(' = ', 1)[1].rstrip(';')
        data = json.loads(page_json)
        tagname = data['entry_data']['TagPage'][0]['graphql']['hashtag']['name']
        tagpic = data['entry_data']['TagPage'][0]['graphql']['hashtag']['profile_pic_url']
        hastag = hastag
        for post in data['entry_data']['TagPage'][0]['graphql']['hashtag']['edge_hashtag_to_media']['edges']:
            intagramcontent.append({
                'image_src': post['node']['thumbnail_resources'][2]['src'],
                'image_comment' : post['node']['edge_media_to_caption']['edges'][0]['node']['text'],
                'image_display_url':post['node']['display_url'],
                'image_like_count':int(post['node']['edge_liked_by']['count']),
                'tagname':tagname,
                'tagpic':tagpic,
                'hastag':hastag,
            })



for objectitem in intagramcontent:

    ic = Intagram(image_src=objectitem['image_src'],
                  image_comment=objectitem['image_comment'],
                  image_display_url=objectitem['image_display_url'],
                  image_like_count=objectitem['image_like_count'],
                  tagname=objectitem['tagname'],
                  tagpic=objectitem['tagpic'],
                  hastag=objectitem['hastag'])
    ic.save()



trackitems = Intagram.objects.all().exclude(crontime=datetime.date.today())
trackitems.delete()