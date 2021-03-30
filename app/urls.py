"""SORM URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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

from django.urls import path
from .views import *
# from django.contrib.auth.views import LoginView()

urlpatterns = [
    # path('', RegisterView.as_view(), name="register"),
    # path('login/', LoginViewclass.as_view(), name="login"),
    # path('logout/', LogoutView.as_view(), name="logout"),
    # path('get/keyword/', AddUserKeyWordView.as_view(), name="KeyWordView"),
    # path('create/keyword/', AddKeywordView.as_view(), name="AddKeyword"),
    # path('keyword/list/', AllKeywordView.as_view(), name="keywordview"),
    # path('keyword/history/', KeywordHistory.as_view(), name="KeywordHistory"),
    # path('all/keyword/history/', history, name="history"),
    #
    # path('keyword/history/lsm/', lst_m, name="lst_m"),
    # path('keyword/history/lsw/', lst_week, name="lst_week"),
    # path('keyword/history/lsd/', yesterday, name="yesterday"),
    # path('date/filter/', date_filter, name="date_filter"),
    #
    # path('users/', user_list, name="user_list"),
    # path('users/search/history/', user_history, name="user_history"),
    # path('users/google/search/', google_search, name="google_search"),
    # path('users/max/search/', max_key, name="max_key"),
    # path('key/search/history/', key_search_history, name="key_search_history"),

]
