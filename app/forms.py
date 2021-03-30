from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django import forms


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100)


class KeywordStoreForm(forms.ModelForm):
    class Meta:
        model = KeywordStore
        fields = ['user', 'key_name', 'count']


class MyKyewordForm(forms.ModelForm):
    class Meta:
        model = MyKeyword
        fields = ['fields']
