# _*_ coding: utf-8 _*_
__author__ = 'Yang Haibo'
__date__ = '2020/5/11 7:46'

from django_filters import rest_framework as filters
from .models import Area


class AreaFilter(filters.FilterSet):
    """
    行政区划过滤器类
    """
    class Meta:
        model = Area
        fields = ['parent']
