# _*_ coding: utf-8 _*_
__author__ = 'Yang Haibo'
__date__ = '2020/5/26 17:36'

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('users:create')
TOKEN_URL = reverse('users:token')


def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


class PublicUserApiTests(TestCase):
    """测试：用户 API（公众）"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_successful(self):
        """测试：传递有效负载创建用户，成功"""
        payload = {
            'mobile': '15257999999',
            'password': '123456',
            'name': '测试用户'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """测试：创建的用户已经存在"""
        payload = {'mobile': '15257999999', 'password': '123456'}
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """测试：密码必须大于5个字符"""
        payload = {'mobile': '15257999999', 'password': 'pw'}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            mobile=payload['mobile']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """测试：为用户创建令牌，成功"""
        payload = {'mobile': '15257999999', 'password': '123456'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """测试：如果用户提供无效身份验证信息，创建令牌，失败"""
        create_user(mobile='15257999999', password='123456')
        payload = {'mobile': '15257999999', 'password': 'wrong'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """测试：如果用户不存在，创建令牌，失败"""
        payload = {'mobile': '15257999999', 'password': '123456'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """测试：如果密码为空，创建令牌，失败"""
        payload = {'mobile': '15257999999', 'password': ''}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


