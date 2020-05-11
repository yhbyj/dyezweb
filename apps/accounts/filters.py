# _*_ coding: utf-8 _*_
__author__ = 'Yang Haibo'
__date__ = '2020/5/10 18:28'

from django_filters import rest_framework as filters
from .models import Account


class AccountFilter(filters.FilterSet):
    """
    用户账户过滤器类
    """
    class Meta:
        model = Account
        fields = ['username', 'date_joined']
