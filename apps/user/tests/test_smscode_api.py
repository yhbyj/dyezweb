# _*_ coding: utf-8 _*_
__author__ = 'Yang Haibo'
__date__ = '2020/5/28 9:59'

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


SMS_CODES_URL = reverse('user:smscode-list')


class PublicSmsCodeApiTests(TestCase):
    """测试：不需要验证就能访问的短信验证码 API（公众）"""

    def setUp(self):
        self.client = APIClient()

    def test_create_sms_code_successful(self):
        """测试：创建短信验证码，成功"""
        payload = {'mobile': '15257911111'}

        res = self.client.post(SMS_CODES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_create_sms_code_invalid(self):
        """测试：通过无效负载创建短信验证码，失败"""
        payload = {'mobile': ''}

        res = self.client.post(SMS_CODES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_sms_code_with_mobile_registered(self):
        """测试：创建短信验证码时，如果手机号码已注册，抛出异常"""
        mobile = '15257911111'
        password = '123456'
        create_user(mobile=mobile, password=password)
        payload = {'mobile': mobile}

        res = self.client.post(SMS_CODES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
