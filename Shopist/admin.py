from django.contrib import admin

# Register your models here.
from .models import Post, UserModel, Blogs

class PostAdmin(admin.ModelAdmin):
    list_display = ('isim','track','user','crontime','url', 'image','no','site','pricedisplay')
admin.site.register(Post, PostAdmin)


class UserModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'imageurl','no','keyword','searchtime','title','price','url','site','serino','pricedisplay')
admin.site.register(UserModel, UserModelAdmin)


class BlogsAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'site', 'url','searchtimeblog')
admin.site.register(Blogs, BlogsAdmin)
