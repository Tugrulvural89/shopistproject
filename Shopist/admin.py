from django.contrib import admin

# Register your models here.
from .models import Post, UserModel

class PostAdmin(admin.ModelAdmin):
    list_display = ('isim','track','user','crontime','url', 'image','no','site','pricedisplay')
admin.site.register(Post, PostAdmin)


class UserModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'imageurl','no','keyword','searchtime','title','price','url','site','serino','pricedisplay')
admin.site.register(UserModel, UserModelAdmin)





