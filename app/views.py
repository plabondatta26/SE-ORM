from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, FormView, RedirectView
from django.contrib.auth.forms import AuthenticationForm
from .forms import *
from django.urls import reverse_lazy
from django.contrib.auth import logout, login, authenticate
from django.views import View
from datetime import datetime, timedelta
from django.http import HttpResponse,JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class RegisterView(CreateView):
    template_name = 'app/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')


class LoginViewclass(View):
    # template_name = 'app/login.html'
    def get(self,request):
        form = LoginForm()
        return render(request,'app/login.html', {'form': form})
    def post(self,request):
        form = LoginForm(request.POST)
        if form.is_valid():
            us = form.cleaned_data['username']
            ps = form.cleaned_data['password']
            user = authenticate(request, username=us, password=ps)
            if user is not None:
                login(request, user)
                return redirect('KeyWordView')
            else:
                return redirect('login')


class LogoutView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')


class AddKeywordView(LoginRequiredMixin, View):
    def get(self, request):
        form = MyKyewordForm()
        return render(request, 'app/addkey.html', {'form': form})

    def post(self, request):
        form = MyKyewordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('keywordview')
        return render(request, 'app/addkey.html', {'form': form})



class AllKeywordView(LoginRequiredMixin, ListView):
    model = MyKeyword
    ordering = ['-id']
    template_name = 'app/keywordslist.html'


class AddUserKeyWordView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        form = KeywordStoreForm()
        return render(request, 'app/key.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = KeywordStoreForm(request.POST)
        form.user = request.user
        user_id = request.user.id

        word_arr = request.POST.get('key_name').split()
        print(word_arr)
        for i in word_arr:
            try:
                key_count = 1
                myk = MyKeyword.objects.get(fields=i.lower())
                key_count += KeywordStore.objects.filter(key_name=i.lower(), user_id=user_id).count()
                KeywordStore.objects.create(user_id=request.user.id, key_name=myk.fields, count=key_count)
            except:
                pass

        return render(request, 'app/key.html', {'form': form})


class KeywordHistory(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'app/history.html')


def yesterday(request):
    now = datetime.now().date()
    last_date = now - timedelta(days=1)
    data = list(KeywordStore.objects.filter(created_on=last_date).order_by('-created_on').values())  # wrap in list(), because QuerySet is not JSON serializable
    return JsonResponse(data, safe=False)


def lst_week(request):
    now = datetime.now().date()
    last_week = now - timedelta(days=7)
    data = list(KeywordStore.objects.filter(created_on__lte=last_week).order_by('-created_on').values())
    return JsonResponse(data, safe=False)


def lst_m(request):
    now = datetime.now().date()
    last_month = now - timedelta(days=30)
    data = list(KeywordStore.objects.filter(created_on__gte=last_month).order_by('-created_on').values())
    return JsonResponse(data, safe=False)


def history(request):
    data_list = list(KeywordStore.objects.all().order_by('-created_on').values())
    return JsonResponse(data_list, safe=False)


def date_filter(request):
    if request.method == 'POST':
        start = request.POST.get('start')
        end = request.POST.get('end')
        data = list(KeywordStore.objects.filter(created_on__range=[start, end]).order_by('-created_on').values())
        return JsonResponse(data, safe=False)


def user_list(request):
    users = list(User.objects.all().order_by('-id').values())
    if request.method == 'POST':
        pass
    return JsonResponse(users, safe=False)

