from django.db import models

# Create your models here.


from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
import datetime
import pytz


class Keyword(models.Model):
    kelime = models.CharField(max_length=250, null=False)
    sites = models.CharField(max_length=250, null=True)
    users = models.CharField(max_length=250, null=True, default="bilinmiyor")
    srptime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.kelime

class Post(models.Model):
    isim = models.CharField(max_length=250, null=True)
    track = models.IntegerField()
    crontime = models.DateTimeField(default=timezone.now)
    url = models.CharField(max_length=550, null=True)
    image = models.CharField(max_length=550, null=True)
    user = models.CharField(max_length=250, null=True)
    no = models.IntegerField()
    site = models.CharField(max_length=250, null=True)
    pricedisplay = models.CharField(max_length=250, null=True)
    serinotrack = models.CharField(max_length=250, null=True, default="234")
    email = models.CharField(max_length=250, null=True, default="tugrulv89@gmail.com")

    def __str__(self):
        return self.isim


class UserModel(models.Model):
    no = models.AutoField(primary_key=True)
    pricedisplay = models.CharField(max_length=250, null=True)
    keyword = models.CharField(max_length=150, default="bilinmiyor")
    title = models.CharField(max_length=150)
    price = models.IntegerField()
    site = models.CharField(max_length=150)
    url = models.CharField(max_length=150)
    searchtime = models.DateTimeField(default=timezone.now)
    imageurl = models.CharField(max_length=450, unique=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
      on_delete=models.CASCADE, null=True
    )
    serino = models.CharField(max_length=150, unique=False)
    email = models.CharField(max_length=250, null=True, default="tugrulv89@gmail.com")

    def __str__(self):
        return self.title


    def __unicode__(self):
        return self.title


class Blogs(models.Model):
    title = models.CharField(max_length=500)
    image = models.CharField(max_length=500)
    site = models.CharField(max_length=500)
    url = models.CharField(max_length=500)
    searchtimeblog = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class Campaign(models.Model):
    title = models.CharField(max_length=500)
    image = models.CharField(max_length=500, null=True)
    site = models.CharField(max_length=500)
    url = models.CharField(max_length=500)
    searchtimeblog = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class UrunInput(models.Model):
    title = models.CharField(max_length=250, null=True)
    price = models.IntegerField()
    crontime = models.DateField(auto_now_add=True)
    url = models.CharField(max_length=550, null=True)
    site = models.CharField(max_length=250, null=True)
    pricedisplay = models.CharField(max_length=250, null=True)
    serino = models.CharField(max_length=250, null=True, default="234")
    kelimearama = models.SlugField(max_length=250, default="bilinmiyor")
    img = models.CharField(max_length=250, null=True)

    def __str__(self):
        return self.title


class Intagram(models.Model):
    tagname = models.CharField(max_length=250, null=True)
    tagpic = models.CharField(max_length=500, null=True)
    image_src = models.CharField(max_length=550, null=True)
    image_comment = models.CharField(max_length=1050, null=True)
    image_display_url = models.CharField(max_length=250, null=True)
    image_like_count = models.IntegerField(null=True, default="234")
    hastag = models.CharField(max_length=250, null=True, default="234")
    crontime = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.tagname



class ContentBlog(models.Model):
    title = models.CharField(max_length=500, null=True)
    image = models.CharField(max_length=500, null=True)
    content = models.CharField(max_length=500, null=True)
    site = models.CharField(max_length=500, null=True)
    slug = models.SlugField(max_length=500)
    crontime = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('contentblogdetail', args=[str(self.slug)])