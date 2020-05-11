# _*_ coding: utf-8 _*_
__author__ = 'Yang Haibo'
__date__ = '2020/5/10 18:27'

from rest_framework import serializers
from .models import Account


# Serializers define the API representation.
class AccountSerializer(serializers.HyperlinkedModelSerializer):
    """
    用户账户序列化类
    """
    class Meta:
        model = Account
        fields = ['url', 'username', 'email', 'is_staff']