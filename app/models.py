from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
# Create your models here.


class KeywordStore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    key_name = models.CharField(max_length=100, blank=True, unique=False)
    count = models.IntegerField(default=1)
    created_on = models.DateField(auto_now_add=True)

    # def save(self, *args, **kwargs):
    #     self.key_name = self.key_name.lower()
    #     return super(KeywordStore, self).save(*args, **kwargs)
    def __str__(self):
        return self.key_name


class MyKeyword(models.Model):
    fields = models.CharField(max_length=100, blank=False, unique=True)

    # def save(self, *args, **kwargs):
    #     self.fields = self.fields.lower()
    #     return super(MyKeyword, self).save(*args, **kwargs)

    def __str__(self):
        return self.fields

