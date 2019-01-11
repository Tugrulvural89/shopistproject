from django.contrib import admin

# Register your models here.
from .models import Post, UserModel, Blogs, Campaign, Keyword, UrunInput, Intagram, ContentBlog, Uyelik, SearchResult




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


class UrunInputAdmin(admin.ModelAdmin):
    list_display = ('title','price','crontime','site','kelimearama')
admin.site.register(UrunInput, UrunInputAdmin)


class IntagramAdmin(admin.ModelAdmin):
    list_display = ('tagname','crontime','image_like_count')
admin.site.register(Intagram, IntagramAdmin)


class ContentBlogAdmin(admin.ModelAdmin):
    list_display = ('title','site','slug')
admin.site.register(ContentBlog, ContentBlogAdmin)


class UyelikAdmin(admin.ModelAdmin):
    pass
admin.site.register(Uyelik, UyelikAdmin)



class SearchResultAdmin(admin.ModelAdmin):
    pass
admin.site.register(SearchResult, SearchResultAdmin)


