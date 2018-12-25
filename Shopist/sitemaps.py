from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from Shopist.models import ContentBlog

class ContentBlogSitemap(Sitemap):
    def items(self):
        return ContentBlog.objects.all()

class StaticViewSitemap(Sitemap):
    def items(self):
        return ['campaign','index','HomePageView','contentblog','profilpage']
    def location(self, obj):
        return reverse(obj)