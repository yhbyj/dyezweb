# _*_ coding: utf-8 _*_
__author__ = 'Yang Haibo'
__date__ = '2020/5/26 17:36'

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import SmsCode

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


class PublicUserApiTests(TestCase):
    """测试：不需要验证就能访问的用户 API（公众）"""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_successful(self):
        """测试：传递有效负载创建用户，成功"""
        mobile = '15257911111'
        sms_code = SmsCode.objects.create(mobile=mobile, code='1234')
        payload = {
            'mobile': mobile,
            'password': '123456',
            'code': sms_code.code
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """测试：创建的用户已经存在"""
        payload = {'mobile': '15257911111', 'password': '123456'}
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """测试：密码必须大于5个字符"""
        payload = {'mobile': '15257911111', 'password': 'pw'}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            mobile=payload['mobile']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """测试：为用户创建令牌，成功"""
        payload = {'mobile': '15257911111', 'password': '123456'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """测试：如果用户提供无效身份验证信息，创建令牌，失败"""
        create_user(mobile='15257911111', password='123456')
        payload = {'mobile': '15257911111', 'password': 'wrong'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """测试：如果用户不存在，创建令牌，失败"""
        payload = {'mobile': '15257911111', 'password': '123456'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """测试：如果密码为空，创建令牌，失败"""
        payload = {'mobile': '15257911111', 'password': ''}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """测试：没有验证，获取用户信息，失败"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """测试：需要验证后，才能访问的用户 API（私有）"""

    def setUp(self) -> None:
        self.user = create_user(
            mobile='15257911111',
            password='123456',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_successful(self):
        """测试：通过验证后，获取用户信息，成功"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'mobile': self.user.mobile
        })

    def test_post_me_not_allowed(self):
        """测试：在 me url 上 post， 失败"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile_successful(self):
        """测试：已登录用户，更新用户信息，成功"""
        payload = {'password': 'newpass'}
        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
