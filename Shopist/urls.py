from . import views
from django.urls import path
from .forms import NameForm
from django.contrib.auth import get_user_model


urlpatterns = [
    path('arama/',views.index,name="index"),
    path('', views.HomePageView, name='HomePageView'),
    path('campaign/', views.campaign, name='campaign'),
    path('profilpage/', views.profilpage, name='profilpage'),
    path('urun/<int:pk>/', views.post_detail, name='post_detail'),
]



