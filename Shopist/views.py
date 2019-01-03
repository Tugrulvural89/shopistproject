from django.shortcuts import render, HttpResponseRedirect, redirect
import requests
from bs4 import BeautifulSoup
from .forms import NameForm, PostForm, DeleteForm, UyeForm
from django.http import HttpResponse
from .models import Post, UserModel, Blogs, Campaign, Keyword, UrunInput, Intagram, ContentBlog, Uyelik
from operator import itemgetter
import datetime
from django.core.mail import send_mail
from django.core.paginator import Paginator
import pytz
import random
from django.core.paginator import Paginator
from django.shortcuts import get_list_or_404, get_object_or_404
# Create your views here.
def index(request):
    newlist=[]
    denemes = []
    intagrams = Intagram.objects.all().order_by("-image_like_count")[0:3]
    if request.method == 'POST':
        form = NameForm(request.POST)
        form1 = PostForm(request.POST)
        uyeform = UyeForm(request.POST)
        if uyeform.is_valid():
            uye = uyeform.save(commit=False)
            uyes = Uyelik(email=uyeform.cleaned_data['email'])
            uyeemail = uyeform.cleaned_data['email']
            send_mail('Kaydın alındı. Teşekkürler!',
                      'Yeni ürünler ve içeriklerden sizleri düzenli olarak haberdar edeceğiz.',
                      'tugrulv@foruandme.com', ['{0}'.format(uyeemail)],
                      fail_silently=False)
            uye.save()
        if form1.is_valid():
            if request.is_ajax():
                post = form1.save(commit=False)
                post.user = request.user
                usermaile = form1.cleaned_data['email']
                send_mail('Yeni Ürün Takibe Alındı!',
                          'Fiyatlarla ilgili detaylara profil sayfandan ulaşabilirsin. Merak etme ürünün indirime girerse ilk seni haberdar edeceğiz:)',
                          'tugrulv@foruandme.com', ['{0}'.format(usermaile)],
                          fail_silently=False)
                post.save()
                return HttpResponse()
        if form.is_valid():
            ck = Keyword(kelime=form.cleaned_data['your_name'],users=request.user,
                         sites=form.cleaned_data["countries"])
            ck.save()
            kelime = form.cleaned_data['your_name']
            sites = form.cleaned_data["countries"]
            if request.user.is_authenticated:
                models = UserModel.objects.filter(user=request.user)
                for model in models:
                     denemes.append(model.serino)
            else:
                models = UserModel.objects.all()
                for model in models:
                     denemes.append(model.serino)
            # H&MBs4
            if "HM" in sites:
                subjecthm = form.cleaned_data['your_name']
                rhm = requests.get("https://www2.hm.com/tr_tr/search-results.html?q="+ subjecthm)
                sourcehm = BeautifulSoup(rhm.content, "lxml")
                newsourcehm = sourcehm.find_all('li', attrs={"class": "product-item"})
                for e in newsourcehm:
                    newlist.append({
                        "title": e.find('h3', class_="item-heading").get_text().strip(),
                        "price": int(e.find('span',class_="price").get_text().replace('TL','').strip().replace(',', '').replace('.', '')),
                        "pricedisplay": e.find('span', class_="price").get_text().replace('TL', '').strip(),
                        "site": "HM",
                        "url": "http://www2.hm.com" + e.find(class_="item-link").attrs['href'],
                        "serino": e.find(class_="hm-product-item").attrs['data-articlecode'],
                        "img": e.find('img', class_="item-image").attrs['data-src'],
                     })
            if "Boyner" in sites:
                subjectboyner = form.cleaned_data['your_name']
                rb = requests.get("https://www.boyner.com.tr/search?searchKey=" + subjectboyner)
                sourceboyner = BeautifulSoup(rb.content, "lxml")
                newboynersource = sourceboyner.find_all('div', attrs={"class":"product-list-item"})
                for b in newboynersource:
                    newlist.append({
                        "title": b.find(class_="product-name").get_text().strip(),
                        "price": int(b.find(class_="cs-amount").get_text().strip().replace('TL','').replace(',','').replace('.','')),
                        "pricedisplay": b.find(class_="cs-amount").get_text().strip().replace('TL', ''),
                        "site": "Boyner",
                        "url": "https://www.boyner.com.tr" + b.find(class_="product-figure").attrs['href'],
                        "serino": b.find(class_="product-figure").attrs['data-id'],
                        "img": b.find('img', class_="lazy").attrs['data-original'],
                    })
            if "Trendyol" in sites:
                subjecttrendyol = form.cleaned_data['your_name']
                rt = requests.get("https://www.trendyol.com/tum--urunler?q=" + subjecttrendyol + "&st=" + subjecttrendyol + " + &qt="  + subjecttrendyol)
                sourcetrendyol = BeautifulSoup(rt.content, "lxml")
                newtrendyolsource = sourcetrendyol.find_all('li', attrs={"class":"pc-wrp"})
                for c in newtrendyolsource[0:6]:
                    newlist.append({
                        "title": c.find(class_="pname").get_text().strip(),
                        "price": int(c.find(class_="prspr").get_text().strip().replace('TL','').replace(',','').replace('.','')),
                        "pricedisplay": c.find(class_="prspr").get_text().strip().replace('TL', ''),
                        "site": "Trendyol",
                        "url": "https://www.trendyol.com/" + c.find(class_="pdlnk").attrs['href'],
                        "serino": c.find(class_="favorite").attrs['data-productid'],
                        "img": c.find('img', class_="primg").get('src'),
                    })
                for c in newtrendyolsource[6::]:
                    newlist.append({
                        "title": c.find(class_="pname").get_text().strip(),
                        "price": int(c.find(class_="prspr").get_text().strip().replace('TL','').replace(',','').replace('.','')),
                        "pricedisplay": c.find(class_="prspr").get_text().strip().replace('TL', ''),
                        "site": "Trendyol",
                        "url": "https://www.trendyol.com/" + c.find(class_="pdlnk").attrs['href'],
                        "serino": c.find(class_="favorite").attrs['data-productid'],
                        "img": c.find('img', class_="primg lazy").attrs['data-original'],
                    })
            if "Zara" in sites:
                subjectzara = form.cleaned_data['your_name']
                vy = requests.get("https://www.zara.com/tr/tr/search?searchTerm=" + subjectzara)
                sourcevy = BeautifulSoup(vy.content, "lxml")
                newvy = sourcevy.find_all('li', class_="product")
                for d in newvy:
                    newlist.append({
                        "title": d.find('a', class_="name _item").get_text(),
                        "price": int(d.find(class_="price _product-price").get_text().strip().replace('TL','').replace(',','').replace('.','')),
                        "pricedisplay": d.find(class_="price _product-price").get_text().strip().replace('TL', ''),
                        "site": "Zara",
                        "url": d.find(class_="item _item").attrs['href'],
                        "serino": d.find('li', class_="product _product").attrs['data-productid'],
                        "img": d.find('img', class_="product-media _img _imageLoaded").get('src'),
                    })
            if "Morhipo" in sites:
                mrpsrp = form.cleaned_data['your_name']
                mrps = requests.get("https://www.morhipo.com/kampanya/arama?q=" + mrpsrp + "&qcat=ps")
                sourcemrsp = BeautifulSoup(mrps.content, "lxml")
                newmrps = sourcemrsp.find_all('li', class_="col-controlled col-xxs-6 col-xs-6 col-sm-4 col-md-4 col-lg-4 column")
                for fs in newmrps:
                    newlist.append({
                        "title": fs.find('div', class_="brand").get_text(),
                        "price": int(fs.find(class_="prd_price").get_text().strip().replace('TL','').replace(',','').replace('.','')),
                        "pricedisplay": fs.find(class_="prd_price").get_text().strip().replace('TL', ''),
                        "site": "Morhipo",
                        "url": "https://www.morhipo.com/" + fs.find('a', class_="js-product").attrs['href'],
                        "serino": fs.find(class_='enhanced-ecommerce-data').attrs['data-productid'],
                        "img": fs.find('img', class_="lazyload").attrs['src'],
                    })
            if "Network" in sites:
                ntw = form.cleaned_data['your_name']
                ntws = requests.get("https://www.network.com.tr/search/" + ntw + "?filterCategoryIDList=684")
                sourcentw = BeautifulSoup(ntws.content, "lxml")
                newntw = sourcentw.find_all(class_="listItem")
                for ntw in newntw:
                    newlist.append({
                        "title": ntw.find('span', class_="secondHead").get_text(),
                        "price": int(ntw.find('span', class_="actualPrice").get_text().strip().replace('TL', '').replace(',',
                                                                                                              '').replace(
                            '.', '')),
                        "pricedisplay": ntw.find('span', class_="actualPrice").get_text().strip().replace('TL', ''),
                        "site": "Network",
                        "url": "https://www.network.com.tr" + ntw.find('a', class_="ecommerceClick").attrs['href'],
                        "serino": ntw.find(class_='ecommerceClick').attrs['data-id'],
                        "img": ntw.find('img', class_="lazy").attrs['data-original'],
                    })
            if "Markafoni" in sites:
                mrk = form.cleaned_data['your_name']
                mrks = requests.get("https://www.markafoni.com/arama?q=" + mrk)
                sourcemrk = BeautifulSoup(mrks.content, "lxml")
                newmrk = sourcemrk.find_all(class_="col-xs-4 pro-product-list-item")
                for mrkfr in newmrk:
                    newlist.append({
                        "title": mrkfr.find(class_="pro-product-title -GTM-product-click-action").get_text(),
                        "price": int(mrkfr.find('div', class_="total-sale-price").attrs['data-sale-price'].strip().replace('TL', '').replace(',','').replace('.', '')),
                        "pricedisplay": mrkfr.find('div', class_="total-sale-price").attrs['data-sale-price'].strip().replace('TL', ''),
                        "site": "Markafoni",
                        "url": "https://www.markafoni.com" + mrkfr.find(class_="pro-product-title -GTM-product-click-action").attrs['href'],
                        "serino": mrkfr.find('div', class_='pro-product').attrs['data-gtm-product-id'],
                        "img": mrkfr.find('img', class_="visible").attrs['data-original'],
                    })
            if len(newlist) >= 1:
                newlist1 = sorted(newlist, key=itemgetter('price'), reverse=False)
            else:
                newlist1 = []
            context = {'form': form, 'form1': form1, 'denemes': denemes, 'models': models,'newlist1': newlist1,
                       'newlist':newlist,'kelime':kelime,'uyeform':uyeform}
            return render(request, 'base.html', context)
        else:
            form = NameForm()
            form1 = PostForm()
        uyeform = UyeForm()
        context = {'form': form,'form1': form1,'intagrams':intagrams,'uyeform':uyeform}
        return render(request, 'base.html', context)
    else:
        form = NameForm()
        form1 = PostForm()
        uyeform = UyeForm()
    context = {'form': form, 'form1': form1,'intagrams':intagrams,'uyeform':uyeform}
    return render(request, 'base.html', context)
def contentblog(request):
    if request.method == 'POST':
        contents_list = ContentBlog.objects.all()
        paginator = Paginator(contents_list, 12)
        page = request.GET.get('page')
        contents = paginator.get_page(page)
        uyeform = UyeForm(request.POST)
        if uyeform.is_valid():
            uye = uyeform.save(commit=False)
            uyes = Uyelik(email=uyeform.cleaned_data['email'])
            uyeemail = uyeform.cleaned_data['email']
            send_mail('Kaydın alındı. Teşekkürler!',
                      'Yeni ürünler ve içeriklerden sizleri düzenli olarak haberdar edeceğiz.',
                      'tugrulv@foruandme.com', ['{0}'.format(uyeemail)],
                      fail_silently=False)
            uye.save()

        context = {'contents': contents,'uyeform':uyeform}
        return render(request, 'contentlist.html', context)
    else:
        contents_list = ContentBlog.objects.all()
        paginator = Paginator(contents_list, 12)
        page = request.GET.get('page')
        contents = paginator.get_page(page)
        uyeform=UyeForm()
        context= {'contents':contents,'uyeform':uyeform}
    return render(request, 'contentlist.html', context)

def contentblogdetail(request, slug=ContentBlog.slug):
    content = get_object_or_404(ContentBlog, slug=slug)
    contents = ContentBlog.objects.all()[0:3]
    instagrams = Intagram.objects.all().order_by("-image_like_count")[0:3]
    #content = ContentBlog.objects.filter(slug=slug)[0:1]

    if request.method == 'POST':
        uyeform = UyeForm(request.POST)
        if uyeform.is_valid():
            uye = uyeform.save(commit=False)
            uyes = Uyelik(email=uyeform.cleaned_data['email'])
            uyeemail = uyeform.cleaned_data['email']
            send_mail('Kaydın alındı. Teşekkürler!',
                     'Yeni ürünler ve içeriklerden sizleri düzenli olarak haberdar edeceğiz.',
                      'tugrulv@foruandme.com', ['{0}'.format(uyeemail)],
                      fail_silently=False)
            uye.save()
        context = {'content': content, 'contents': contents, 'instagrams': instagrams,'uyeform':uyeform}
        return render(request, 'contentlistdetail.html', context)
    else:
        uyeform = UyeForm()
        context = {'content': content, 'contents': contents, 'instagrams': instagrams,'uyeform':uyeform}
        return render(request, 'contentlistdetail.html', context)


def HomePageView(request):
    trackitems = UrunInput.objects.all()[0:6]
    blogs = Blogs.objects.all()[0:6]
    contents = ContentBlog.objects.all()[0:6]
    keywords = Keyword.objects.all().order_by("kelime")[0:6]
    campaings = Campaign.objects.all().order_by("-title")[0:6]
    form = NameForm()
    uyeform = UyeForm()
    newlist=[]
    denemes = []
    if request.method == 'POST':
        form = NameForm(request.POST)
        form1 = PostForm(request.POST)
        uyeform = UyeForm(request.POST)
        if uyeform.is_valid():
            uye = uyeform.save(commit=False)
            uyes = Uyelik(email=uyeform.cleaned_data['email'])
            uyeemail = uyeform.cleaned_data['email']
            send_mail('Kaydın alındı. Teşekkürler!',
                      'Yeni ürünler ve içeriklerden sizleri düzenli olarak haberdar edeceğiz.',
                      'tugrulv@foruandme.com', ['{0}'.format(uyeemail)],
                      fail_silently=False)
            uye.save()

        if form1.is_valid():

            uyeform = UyeForm()
            usermaile = form1.cleaned_data['email']
            send_mail('Yeni Ürün Takibe Alındı!',
                      'Fiyatlarla ilgili detaylara profil sayfandan ulaşabilirsin. ürün indirime girdiğinde ilk seni haberdar edeceğiz:)',
                      'tugrulv@foruandme.com', ['{0}'.format(usermaile)],
                      fail_silently=False)
            if request.is_ajax():
                post = form1.save(commit=False)
                post.user = request.user
                post.save()
                return HttpResponse()
        if form.is_valid():

            uyeform = UyeForm()
            ck = Keyword(kelime=form.cleaned_data['your_name'], users=request.user,
                         sites=form.cleaned_data["countries"])
            ck.save()
            kelime = form.cleaned_data['your_name']
            sites = form.cleaned_data["countries"]
            if request.user.is_authenticated:
                models = UserModel.objects.filter(user=request.user)
                for model in models:
                    denemes.append(model.serino)
            else:
                models = UserModel.objects.all()
                for model in models:
                    denemes.append(model.serino)
            # H&MBs4
            if "HM" in sites:
                subjecthm = form.cleaned_data['your_name']
                rhm = requests.get("https://www2.hm.com/tr_tr/search-results.html?q=" + subjecthm)
                sourcehm = BeautifulSoup(rhm.content, "lxml")
                newsourcehm = sourcehm.find_all('li', attrs={"class": "product-item"})
                for e in newsourcehm:
                    newlist.append({
                        "title": e.find('h3', class_="item-heading").get_text().strip(),
                        "price": int(e.find('span', class_="price").get_text().replace('TL', '').strip().replace(',',
                                                                                                                 '').replace(
                            '.', '')),
                        "pricedisplay": e.find('span', class_="price").get_text().replace('TL', '').strip(),
                        "site": "HM",
                        "url": "http://www2.hm.com" + e.find(class_="item-link").attrs['href'],
                        "serino": e.find(class_="hm-product-item").attrs['data-articlecode'],
                        "img": e.find('img', class_="item-image").attrs['data-src'],
                    })
            if "Boyner" in sites:
                subjectboyner = form.cleaned_data['your_name']
                rb = requests.get("https://www.boyner.com.tr/search?searchKey=" + subjectboyner)
                sourceboyner = BeautifulSoup(rb.content, "lxml")
                newboynersource = sourceboyner.find_all('div', attrs={"class": "product-list-item"})
                for b in newboynersource:
                    newlist.append({
                        "title": b.find(class_="product-name").get_text().strip(),
                        "price": int(
                            b.find(class_="cs-amount").get_text().strip().replace('TL', '').replace(',', '').replace(
                                '.', '')),
                        "pricedisplay": b.find(class_="cs-amount").get_text().strip().replace('TL', ''),
                        "site": "Boyner",
                        "url": "https://www.boyner.com.tr" + b.find(class_="product-figure").attrs['href'],
                        "serino": b.find(class_="product-figure").attrs['data-id'],
                        "img": b.find('img', class_="lazy").attrs['data-original'],
                    })
            if "Trendyol" in sites:
                subjecttrendyol = form.cleaned_data['your_name']
                rt = requests.get(
                    "https://www.trendyol.com/tum--urunler?q=" + subjecttrendyol + "&st=" + subjecttrendyol + " + &qt=" + subjecttrendyol)
                sourcetrendyol = BeautifulSoup(rt.content, "lxml")
                newtrendyolsource = sourcetrendyol.find_all('li', attrs={"class": "pc-wrp"})
                for c in newtrendyolsource[0:6]:
                    newlist.append({
                        "title": c.find(class_="pname").get_text().strip(),
                        "price": int(
                            c.find(class_="prspr").get_text().strip().replace('TL', '').replace(',', '').replace('.',
                                                                                                                 '')),
                        "pricedisplay": c.find(class_="prspr").get_text().strip().replace('TL', ''),
                        "site": "Trendyol",
                        "url": "https://www.trendyol.com/" + c.find(class_="pdlnk").attrs['href'],
                        "serino": c.find(class_="favorite").attrs['data-productid'],
                        "img": c.find('img', class_="primg").get('src'),
                    })
                for c in newtrendyolsource[6::]:
                    newlist.append({
                        "title": c.find(class_="pname").get_text().strip(),
                        "price": int(
                            c.find(class_="prspr").get_text().strip().replace('TL', '').replace(',', '').replace('.',
                                                                                                                 '')),
                        "pricedisplay": c.find(class_="prspr").get_text().strip().replace('TL', ''),
                        "site": "Trendyol",
                        "url": "https://www.trendyol.com/" + c.find(class_="pdlnk").attrs['href'],
                        "serino": c.find(class_="favorite").attrs['data-productid'],
                        "img": c.find('img', class_="primg lazy").attrs['data-original'],
                    })
            if "Zara" in sites:
                subjectzara = form.cleaned_data['your_name']
                vy = requests.get("https://www.zara.com/tr/tr/search?searchTerm=" + subjectzara)
                sourcevy = BeautifulSoup(vy.content, "lxml")
                newvy = sourcevy.find_all('li', class_="product")
                for d in newvy:
                    newlist.append({
                        "title": d.find('a', class_="name _item").get_text(),
                        "price": int(
                            d.find(class_="price _product-price").get_text().strip().replace('TL', '').replace(',',
                                                                                                               '').replace(
                                '.', '')),
                        "pricedisplay": d.find(class_="price _product-price").get_text().strip().replace('TL', ''),
                        "site": "Zara",
                        "url": d.find(class_="item _item").attrs['href'],
                        "serino": d.find('li', class_="product _product").attrs['data-productid'],
                        "img": d.find('img', class_="product-media _img _imageLoaded").get('src'),
                    })
            if "Morhipo" in sites:
                mrpsrp = form.cleaned_data['your_name']
                mrps = requests.get("https://www.morhipo.com/kampanya/arama?q=" + mrpsrp + "&qcat=ps")
                sourcemrsp = BeautifulSoup(mrps.content, "lxml")
                newmrps = sourcemrsp.find_all('li',
                                              class_="col-controlled col-xxs-6 col-xs-6 col-sm-4 col-md-4 col-lg-4 column")
                for fs in newmrps:
                    newlist.append({
                        "title": fs.find('div', class_="brand").get_text(),
                        "price": int(
                            fs.find(class_="prd_price").get_text().strip().replace('TL', '').replace(',', '').replace(
                                '.', '')),
                        "pricedisplay": fs.find(class_="prd_price").get_text().strip().replace('TL', ''),
                        "site": "Morhipo",
                        "url": "https://www.morhipo.com/" + fs.find('a', class_="js-product").attrs['href'],
                        "serino": fs.find(class_='enhanced-ecommerce-data').attrs['data-productid'],
                        "img": fs.find('img', class_="lazyload").attrs['src'],
                    })
            if "Network" in sites:
                ntw = form.cleaned_data['your_name']
                ntws = requests.get("https://www.network.com.tr/search/" + ntw + "?filterCategoryIDList=684")
                sourcentw = BeautifulSoup(ntws.content, "lxml")
                newntw = sourcentw.find_all(class_="listItem")
                for ntw in newntw:
                    newlist.append({
                        "title": ntw.find('span', class_="secondHead").get_text(),
                        "price": int(
                            ntw.find('span', class_="actualPrice").get_text().strip().replace('TL', '').replace(',',
                                                                                                                '').replace(
                                '.', '')),
                        "pricedisplay": ntw.find('span', class_="actualPrice").get_text().strip().replace('TL', ''),
                        "site": "Network",
                        "url": "https://www.network.com.tr" + ntw.find('a', class_="ecommerceClick").attrs['href'],
                        "serino": ntw.find(class_='ecommerceClick').attrs['data-id'],
                        "img": ntw.find('img', class_="lazy").attrs['data-original'],
                    })
            if "Markafoni" in sites:
                mrk = form.cleaned_data['your_name']
                mrks = requests.get("https://www.markafoni.com/arama?q=" + mrk)
                sourcemrk = BeautifulSoup(mrks.content, "lxml")
                newmrk = sourcemrk.find_all(class_="col-xs-4 pro-product-list-item")
                for mrkfr in newmrk:
                    newlist.append({
                        "title": mrkfr.find(class_="pro-product-title -GTM-product-click-action").get_text(),
                        "price": int(
                            mrkfr.find('div', class_="total-sale-price").attrs['data-sale-price'].strip().replace('TL',
                                                                                                                  '').replace(
                                ',', '').replace('.', '')),
                        "pricedisplay": mrkfr.find('div', class_="total-sale-price").attrs[
                            'data-sale-price'].strip().replace('TL', ''),
                        "site": "Markafoni",
                        "url": "https://www.markafoni.com" +
                               mrkfr.find(class_="pro-product-title -GTM-product-click-action").attrs['href'],
                        "serino": mrkfr.find('div', class_='pro-product').attrs['data-gtm-product-id'],
                        "img": mrkfr.find('img', class_="visible").attrs['data-original'],
                    })
            if len(newlist) >= 1:
                newlist1 = sorted(newlist, key=itemgetter('price'), reverse=False)
            else:
                newlist1 = []
            context = {'form': form, 'form1': form1,'uyeform':uyeform, 'denemes': denemes, 'models': models, 'newlist1': newlist1,
                       'newlist': newlist,'blogs':blogs,
                       'keywords':keywords,'campaings':campaings,'contents':contents,"trackitems":trackitems}
            return render(request, 'base.html', context)
        else:
            context = {'blogs': blogs, 'form': form,'uyeform':uyeform,
                       'keywords':keywords,'campaings':campaings,'contents':contents,"trackitems":trackitems}
            return render(request, 'home.html', context)
    else:
        intagrams = Intagram.objects.all().order_by("-image_like_count")[0:6]
        uyeform = UyeForm()
        context = {'blogs':blogs,'form':form,'uyeform':uyeform,
                       'keywords':keywords,'campaings':campaings,'intagrams':intagrams,'contents':contents,"trackitems":trackitems}
        return render(request, 'home.html', context)
def profilpage(request):
    profil = UserModel.objects.filter(user=request.user)
    if request.method == 'POST':
        form1 = DeleteForm(request.POST)
        uyeform = UyeForm(request.POST)
        if form1.is_valid():
            deleteserino = form1.cleaned_data['deleteserino']
            if request.is_ajax():
                user = request.user
                postmodel = Post.objects.filter(no=deleteserino)
                postmodel.delete()
                profil1 = UserModel.objects.filter(no=deleteserino)
                profil1.delete()
                return HttpResponse()

        if uyeform.is_valid():
            uye = uyeform.save(commit=False)
            uyes = Uyelik(email=uyeform.cleaned_data['email'])
            uyeemail = uyeform.cleaned_data['email']
            send_mail('Kaydın alındı. Teşekkürler!',
                      'Yeni ürünler ve içeriklerden sizleri düzenli olarak haberdar edeceğiz.',
                      'tugrulv@foruandme.com', ['{0}'.format(uyeemail)],
                      fail_silently=False)
            uye.save()
        context = {'profil': profil,'uyeform':uyeform}
        return render(request, 'profilpage.html', context)
    else:
        uyeform = UyeForm()
        context= {'profil':profil,'uyeform':uyeform}
        return render(request, 'profilpage.html', context)
def post_detail(request, pk):
    tracks =Post.objects.filter(no=pk)
    profils = UserModel.objects.filter(no=pk)
    uyeform = UyeForm()
    if request.method == 'POST':
        uyeform = UyeForm(request.POST)
        if uyeform.is_valid():
            uye = uyeform.save(commit=False)
            uye = Uyelik(email=uyeform.cleaned_data['email'])
            uyeemail = uyeform.cleaned_data['email']
            send_mail('Kaydın alındı. Teşekkürler!',
                      'Yeni ürünler ve içeriklerden sizleri düzenli olarak haberdar edeceğiz.',
                      'tugrulv@foruandme.com', ['{0}'.format(uyeemail)],
                      fail_silently=False)
            uye.save()
        return render(request, 'profildetailpage.html', {'tracks': tracks, 'profils': profils,'uyeform':uyeform})
    else:
        uyeform = UyeForm()
        return render(request, 'profildetailpage.html', {'tracks': tracks, 'profils': profils,'uyeform':uyeform})
def campaign(request):
    homelist = Campaign.objects.all().order_by('title').filter(searchtimeblog=datetime.date.today())
    basedsite = Campaign.objects.all().order_by('site').filter(searchtimeblog=datetime.date.today())
    uyeform = UyeForm()
    if request.method == 'POST':
        uyeform = UyeForm(request.POST)
        if uyeform.is_valid():
            uye = uyeform.save(commit=False)
            uyes = Uyelik(email=uyeform.cleaned_data['email'])
            uyeemail = uyeform.cleaned_data['email']
            send_mail('Kaydın alındı. Teşekkürler!',
                      'Yeni ürünler ve içeriklerden sizleri düzenli olarak haberdar edeceğiz.',
                      'tugrulv@foruandme.com', ['{0}'.format(uyeemail)],
                      fail_silently=False)
            uye.save()
        context = {'homelist': homelist, 'basedsite': basedsite, 'uyeform': uyeform}
        return render(request, 'campaign.html', context)
    else:
        uyeform = UyeForm()
        context= {'homelist':homelist,'basedsite':basedsite,'uyeform':uyeform}
        return render(request, 'campaign.html', context)

def urunsayfa(request, slug=UrunInput.kelimearama):
    denemes = []
    form1 = PostForm()
    uruns = UrunInput.objects.filter(kelimearama=slug)
    uyeform = UyeForm()
    if request.user.is_authenticated:
        models = UserModel.objects.filter(user=request.user)
        for model in models:
            denemes.append(model.serino)
    else:
        models = UserModel.objects.all()
        for model in models:
            denemes.append(model.serino)

    if request.method == 'POST':
        form1 = PostForm(request.POST)
        uyeform = UyeForm(request.POST)
        if uyeform.is_valid():
            uye = uyeform.save(commit=False)
            uyes = Uyelik(email=uyeform.cleaned_data['email'])
            uyeemail = uyeform.cleaned_data['email']
            send_mail('Kaydın alındı. Teşekkürler!',
                      'Yeni ürünler ve içeriklerden sizleri düzenli olarak haberdar edeceğiz.',
                      'tugrulv@foruandme.com', ['{0}'.format(uyeemail)],
                      fail_silently=False)
            uye.save()
        if form1.is_valid():
            if request.is_ajax():
                post = form1.save(commit=False)
                post.user = request.user
                post.save()
                return HttpResponse()
    context= {'uruns':uruns,
              'denemes':denemes,
              'models':models,'form1':form1, 'uyeform':uyeform}
    return render(request, 'input.html', context)