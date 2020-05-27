# _*_ coding: utf-8 _*_
__author__ = 'Yang Haibo'
__date__ = '2020/5/26 21:32'

from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """用户对象序列化类"""

    class Meta:
        model = get_user_model()
        fields = ('mobile', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """创建一个带加密密码的新用户并返回"""
        return get_user_model().objects.create_user(**validated_data)


class AuthTokenSerializer(serializers.Serializer):
    """令牌对象序列化"""
    mobile = serializers.CharField(max_length=11, label='手机号码')
    password = serializers.CharField(
        min_length=5,
        style={'input_type': 'password'},
        trim_whitespace=False,
        label='密码'
    )

    def validate(self, attrs):
        """验证用户的有效性"""
        mobile = attrs.get('mobile')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=mobile,
            password=password
        )
        if not user:
            msg = _('无法根据提供的机密信息通过用户验证')
            # msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return attrs