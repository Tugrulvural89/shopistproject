from django.contrib import admin

# Register your models here.
from .models import Post, UserModel, Blogs, Campaign, Keyword




class PostAdmin(admin.ModelAdmin):
    list_display = ('isim','track','user','crontime','url', 'image','no','site','pricedisplay','email')
admin.site.register(Post, PostAdmin)


class UserModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'imageurl','no','keyword','searchtime','title','price','url','site','serino','pricedisplay')
admin.site.register(UserModel, UserModelAdmin)


class BlogsAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'site', 'url','searchtimeblog')
admin.site.register(Blogs, BlogsAdmin)


class CampaignAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'site', 'url','searchtimeblog')
admin.site.register(Campaign, CampaignAdmin)


class KeywordAdmin(admin.ModelAdmin):
    list_display = ('kelime','srptime','sites','users')
admin.site.register(Keyword, KeywordAdmin)


