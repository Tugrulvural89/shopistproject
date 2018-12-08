from django import forms
from django.forms import ModelForm
from .models import Post, UserModel
from django.contrib.auth import get_user_model

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)

    OPTIONS = (
        ("Boyner", "Boyner"),
        ("HM", "HM"),
        ("Trendyol", "Trendyol"),
        ("Zara", "Zara"),
        ("Morhipo", "Morhipo"),
        ("Network", "Network"),
        ("Markafoni", "Markafoni"),
    )
    countries = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=OPTIONS)

class PostForm(ModelForm):
    #usermodel oluşturulup customuser managerden foreing key olarak çekildi.
    #itemi sadece form olarak html üzerinden hidden alıyoruz.
    class Meta:
        model = UserModel
        fields = ['imageurl','keyword','title','price','url','site','serino','pricedisplay','email']
        widgets = {'imageurl': forms.HiddenInput(),
                   'keyword': forms.HiddenInput(),
                   'price': forms.HiddenInput(),
                   'title': forms.HiddenInput(),
                   'site': forms.HiddenInput(),
                   'url': forms.HiddenInput(),
                   'serino': forms.HiddenInput(),
                   'user': forms.HiddenInput(),
                   'pricedisplay':forms.HiddenInput(),
                   'email': forms.HiddenInput(),
                   }


class DeleteForm(forms.Form):
    deleteserino = forms.CharField(label='deleteserino', max_length=100)
    widgets = {'deleteserino': forms.HiddenInput(),}





class PriceForm(forms.Form):
        OPTIONS = (
            ("AUT", "Austria"),
            ("DEU", "Germany"),
            ("NLD", "Neitherlands"),
        )
        Countries = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                              choices=OPTIONS)