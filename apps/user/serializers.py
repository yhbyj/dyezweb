# _*_ coding: utf-8 _*_
__author__ = 'Yang Haibo'
__date__ = '2020/5/26 21:32'

import re

from django.conf import settings
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from rest_framework import serializers

from core.models import SmsCode


class UserSerializer(serializers.ModelSerializer):
    """用户对象序列化类"""
    # 如果没有设置 write_only=True， post 后用户能创建成功，
    # 但是浏览器会显示错误，因为 code 被排除掉了，序列化失败。
    code = serializers.CharField(required=True, min_length=4,
                                 max_length=4, label='验证码',
                                 help_text='必填。4位的数字。',
                                 write_only=True)

    # write_only=True， 只写入数据库，不序列化返回
    password = serializers.CharField(style={'input_type': 'password'},
                                     label='密码', write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('mobile', 'password', 'code',)
        extra_kwargs = {'mobile': {'min_length': 11, 'max_length': 11}}

    def validate_code(self, code):
        # 按添加的时间，降序排列筛选出来的验证码，获得最近的验证码。
        sms_codes = SmsCode.objects.filter(
            mobile=self.initial_data['mobile']
        ).order_by('-add_time')
        if sms_codes:
            # 获取最新的一条
            last_sms_code = sms_codes[0]
            # 验证码有效期为30分钟
            five_minutes_ago = timezone.now() - timezone.timedelta(days=0,
                                                                   minutes=30,
                                                                   seconds=0)
            if last_sms_code.add_time < five_minutes_ago:
                raise serializers.ValidationError('验证码过期')
            if last_sms_code.code != code:
                raise serializers.ValidationError('验证码错误')
        else:
            raise serializers.ValidationError('验证码未发送')

    # def validate(self, attrs):
    #     # 丢弃不需要存入数据库的验证码
    #     del attrs['code']
    #     return attrs

    def create(self, validated_data):
        """创建一个带加密密码的新用户并返回"""
        # 丢弃不需要存入数据库的验证码
        validated_data.pop('code')
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """更新用户，密码设置正确，并返回用户"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


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


class SmsCodeSerializer(serializers.ModelSerializer):
    """短信验证码序列化类"""

    def validate_mobile(self, mobile):
        """验证手机号码(函数名称必须为validate_ + 字段名)"""
        # 手机号码是否注册
        if get_user_model().objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("该手机号码已注册")

        # 验证手机号码是否合法
        if not re.match(settings.REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法")

        # 验证码发送频率
        one_minutes_ago = timezone.now() - timezone.timedelta(hours=0,
                                                              minutes=1,
                                                              seconds=0)
        # 添加时间大于一分钟以前。也就是距离现在还不足一分钟
        if SmsCode.objects.filter(
                add_time__gt=one_minutes_ago, mobile=mobile
        ).count():
            raise serializers.ValidationError("距离上一次发送未超过60s")

        return mobile

    class Meta:
        model = SmsCode
        fields = ('id', 'mobile', )
        read_only_fields = ('id',)
