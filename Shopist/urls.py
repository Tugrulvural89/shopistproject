from . import views
from django.urls import path


urlpatterns = [
    path('', views.HomePageView, name='HomePageView'),
    path('arama/',views.index,name="index"),
    path('campaign/', views.campaign, name='campaign'),
    path('profilpage/', views.profilpage, name='profilpage'),
    path('takip/<int:pk>/', views.post_detail, name='post_detail'),
    path('urun/', views.urunsayfas, name='urunsayfas'),
    path('urun/<slug>/', views.urunsayfa, name='urunsayfa'),
    path('blog/', views.contentblog, name='contentblog'),
    path('blog/<slug>/', views.contentblogdetail, name='contentblogdetail'),
    path('intagram/', views.inputtags, name='inputtags'),
]




