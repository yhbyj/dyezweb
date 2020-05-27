# _*_ coding: utf-8 _*_
__author__ = 'Yang Haibo'
__date__ = '2020/5/25 7:26'

from django.contrib.auth import get_user_model
from django.test import TestCase


class ModelTests(TestCase):

    def test_create_user_with_mobile_phone_number_successful(self):
        """测试：用移动电话号码创建用户，成功"""
        mobile = '15257999999'
        password = '123456'
        user = get_user_model().objects.create_user(
            mobile=mobile,
            password=password
        )

        self.assertEqual(user.mobile, mobile)
        self.assertTrue(user.check_password(password))

    def test_new_user_invalid_mobile(self):
        """测试：创建新用户时，没有用户名，抛出异常"""
        mobile = None
        password = '123456'
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                mobile=mobile,
                password=password
            )

    def test_create_new_superuser(self):
        """测试：创建超级用户，成功"""
        mobile = '15257999999'
        password = '123456'
        user = get_user_model().objects.create_superuser(
            mobile=mobile,
            password=password
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
