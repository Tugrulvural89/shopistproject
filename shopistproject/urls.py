"""shopistproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include
from django.conf import settings
from Shopist.sitemaps import ContentBlogSitemap, StaticViewSitemap

sitemaps = {
    'content': ContentBlogSitemap,
    'static': StaticViewSitemap,
}

urlpatterns = [
    path('sitemap.xml',sitemap,{'sitemaps':sitemaps}),
    path('robots.txt', include('robots.urls')),
    path('', include('Shopist.urls')),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]

