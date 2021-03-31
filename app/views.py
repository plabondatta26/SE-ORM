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
from django.db.models import Max
from googlesearch import search
from heapq import nlargest
from datetime import datetime
from .serializer import KeywordStoreSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView
now = datetime.now().date()
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


def google_search(k):
    result_list = []
    x = search(k, num_results=10, lang="en")
    for i in range(0, 5):
        result_list.append(x[i])
    result ={
        'data': result_list
    }
    return result


class AddUserKeyWordView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        form = KeywordStoreForm()
        return render(request, 'app/key.html', {'form': form})

    def post(self, request):
        user_id = request.user.id
        k = request.POST.get('key_name')
        data = google_search(k)
        word_arr = k.split()
        for i in word_arr:
            try:
                key_count = 1
                myk = MyKeyword.objects.get(fields=i.lower())
                kc = KeywordStore.objects.filter(key_name=i.lower(), user=user_id).count()
                print(kc)
                if kc is not None:
                    key_count += kc
                KeywordStore.objects.create(key_name=i.lower(), user_id=user_id, count=key_count)

            except:
                pass
        return JsonResponse(data, safe=False)


class KeywordHistory(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'app/history.html')


class Yesterday(ListAPIView):
    serializer_class = KeywordStoreSerializer

    def get_queryset(self):
        queryset = KeywordStore.objects.all()
        yesterday = now - timedelta(days=1)
        queryset = queryset.filter(created_on__gte=yesterday)
        return queryset


class LastWeek(ListAPIView):
    serializer_class = KeywordStoreSerializer

    def get_queryset(self):
        queryset = KeywordStore.objects.all()
        last_week = now - timedelta(days=7)

        if last_week is not None:
            queryset = queryset.filter(created_on__gte=last_week).order_by('-created_on')
        return queryset


class LastMonth(ListAPIView):
    serializer_class = KeywordStoreSerializer

    def get_queryset(self):
        queryset = KeywordStore.objects.all()
        last_month = now - timedelta(days=30)

        if last_month is not None:
            queryset = queryset.filter(created_on__gte=last_month).order_by('-created_on')
        return queryset


@api_view(['GET'])
def history(request):
    ks = KeywordStore.objects.all().order_by('-created_on')
    serialize = KeywordStoreSerializer(ks, many=True)
    return Response(serialize.data)


class DateFilter(ListAPIView):
    serializer_class = KeywordStoreSerializer

    def get_queryset(self):
        queryset = KeywordStore.objects.all()
        st = self.request.query_params.get('start')
        en = self.request.query_params.get('end')

        if st and en is not None:
            queryset = queryset.filter(created_on__gte=st, created_on__lte=en).order_by('-created_on')
        return queryset


def user_list(request):
    users = list(User.objects.all().order_by('-id').values())
    return JsonResponse(users, safe=False)


class UserHistory(ListAPIView):
    serializer_class = KeywordStoreSerializer

    def get_queryset(self):
        queryset = KeywordStore.objects.all()
        us = self.request.query_params.get('data_id')
        if us is not None:
            queryset = queryset.filter(user=us).order_by('-created_on')
        return queryset


def max_key(request):
    myk = []
    storedk = []
    keys = []
    values = []
    data = []
    max_val = []
    k = MyKeyword.objects.all()
    for i in k:
        myk.append(i.fields)
    for j in myk:
        x = KeywordStore.objects.filter(key_name=j).last()
        storedk.append(x)
    for m in storedk:
        if m is not None:
            keys.append(m.key_name)
            values.append(m.count)

    data = dict(zip(keys, values))
    keys = sorted(data, key=data.get, reverse=True)[:3]
    for i in keys:
        max_val.append(data[i])
    data = dict(zip(keys, max_val))
    return JsonResponse(data, safe=False)


class KeySearchHistory(ListAPIView):
    serializer_class = KeywordStoreSerializer

    def get_queryset(self):
        queryset = KeywordStore.objects.all()
        kw = self.request.query_params.get('key_name')
        if kw is not None:
            queryset = queryset.filter(key_name=kw).order_by('-created_on')
        return queryset
