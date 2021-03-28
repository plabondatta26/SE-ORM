from django.contrib import admin
from .models import KeywordStore, MyKeyword
# Register your models here.

admin.site.register(KeywordStore)
admin.site.register(MyKeyword)
