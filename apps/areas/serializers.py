# _*_ coding: utf-8 _*_
__author__ = 'Yang Haibo'
__date__ = '2020/5/11 7:46'

from rest_framework import serializers
from .models import Area


# Serializers define the API representation.
class AreaSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = '__all__'


class AreaSerializer(serializers.ModelSerializer):
    """
    行政区划数据序列化类
    """
    subs = AreaSerializer2(many=True)
    class Meta:
        model = Area
        fields = '__all__'
