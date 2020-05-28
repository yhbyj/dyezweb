# _*_ coding: utf-8 _*_
__author__ = 'Yang Haibo'
__date__ = '2020/5/26 21:32'

from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from core.models import Tag


class TagSerializer(serializers.ModelSerializer):
    """标签对象序列化"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)
