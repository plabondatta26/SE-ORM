from .models import KeywordStore, MyKeyword
from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class KeywordStoreSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = KeywordStore
        fields = '__all__'
