from django import forms
from django.forms import ModelForm
from .models import Post, UserModel, Uyelik
from django.contrib.auth import get_user_model

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100, required=True)

    OPTIONS = (
        ("Boyner", "Boyner"),
        ("HM", "HM"),
        ("Trendyol", "Trendyol"),
        ("Nike", "Nike"),
        ("Morhipo", "Morhipo"),
        ("Network", "Network"),
        ("Markafoni", "Markafoni"),
        ("ipekyol", "İpekyol"),

    )
    countries = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                          choices=OPTIONS,required=True)

    OPTIONS1 = (
        ("3", "Sana En Uygun"),
        ("2", "Ucuzdan Pahalıya"),
        ("1", "Pahalıdan Ucuza"),
    )
    sira = forms.ChoiceField(choices=OPTIONS1, label="",required=False)


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

class UyeForm(ModelForm):
    #usermodel oluşturulup customuser managerden foreing key olarak çekildi.
    #itemi sadece form olarak html üzerinden hidden alıyoruz.
    class Meta:
        model = Uyelik
        fields = ['email']

class DeleteForm(forms.Form):
    deleteserino = forms.CharField(label='deleteserino', max_length=100)
    widgets = {'deleteserino': forms.HiddenInput(),}




class PriceForm(forms.Form):
        OPTIONS = (
            ("1", "Pahalıdan Ucuza"),
            ("2", "Ucuzdan Pahalıya"),
        )
        sira = forms.ChoiceField(choices=OPTIONS, label="")
