# _*_ coding: utf-8 _*_
__author__ = 'Yang Haibo'
__date__ = '2020/5/10 18:27'

import re
from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from dyezweb.settings import REGEX_MOBILE
from .models import Account, SmsCode

User = get_user_model()


# Serializers define the API representation.
class AccountRegSerializer(serializers.ModelSerializer):
    """
    用户账户注册序列化类
    """
    # 如果没有设置 write_only=True， post 后用户能创建成功，
    # 但是浏览器会显示错误，因为 code 被排除掉了，序列化失败。
    code = serializers.CharField(required=True, min_length=4, max_length=4, label='验证码',
                                 help_text='必填。4位的数字。', write_only=True)

    username = serializers.CharField(label="用户名", help_text="请用手机号码作为用户填写！", required=True, allow_blank=False,
                                     validators=[UniqueValidator(queryset=Account.objects.all(), message="用户已经存在")])

    # 如果没有设置 read_only=True， 会在表单中显示该字段，而这是不需要的。
    # 但可以被 get
    mobile = serializers.CharField(read_only=True)

    # write_only=True， 只写入数据库，不序列化返回
    password = serializers.CharField(style={'input_type': 'password'}, label='密码', write_only=True)

    def validated_code(self, code):
        # 用户在前端注册时，手机号作为用户名传递过来。
        # 按添加的时间，降序排列筛选出来的验证码，获得最近的验证码。
        smscodes = SmsCode.objects.filter(mobile=self.initial_data['username']).order_by('-add_time')
        if smscodes:
            # 获取最新的一条
            last_smscode = smscodes[0]
            # 验证码有效期为30分钟
            five_minutes_ago = datetime.now() - timedelta(days=0, minutes=30, seconds=0)
            if last_smscode.add_time < five_minutes_ago:
                raise serializers.ValidationError('验证码过期')
            if last_smscode.code != code:
                raise serializers.ValidationError('验证码错误')
        else:
            raise serializers.ValidationError('验证码未发送')

    def validate(self, attrs):
        # 验证通过之后，把以用户名方式传过来的手机号填入相应属性。
        attrs['mobile'] = attrs['username']
        # 丢弃不需要存入数据库的验证码
        del attrs['code']
        return attrs

    def create(self, validated_data):
        account = super(AccountRegSerializer, self).create(validated_data=validated_data)
        account.set_password(validated_data['password'])
        account.save()
        return account

    class Meta:
        model = Account
        fields = ['username', 'code', 'mobile', 'password']


class SmsCodeSerializer(serializers.ModelSerializer):
    """
    短信验证码序列化类
    """

    def validate_mobile(self, mobile):
        """
        验证手机号码(函数名称必须为validate_ + 字段名)
        """
        # 手机号码是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("该手机号码已注册")

        # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法")

        # 验证码发送频率
        one_minutes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        # 添加时间大于一分钟以前。也就是距离现在还不足一分钟
        if SmsCode.objects.filter(add_time__gt=one_minutes_ago, mobile=mobile).count():
            raise serializers.ValidationError("距离上一次发送未超过60s")

        return mobile

    class Meta:
        model = SmsCode
        fields = ['mobile']