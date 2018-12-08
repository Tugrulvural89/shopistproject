from django.db import models

# Create your models here.


from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

class Post(models.Model):
    isim = models.CharField(max_length=250, null=True)
    track = models.DecimalField(max_digits=6, decimal_places=2)
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
    keyword = models.CharField(max_length=150)
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
    searchtimeblog = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title