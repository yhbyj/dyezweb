# _*_ coding: utf-8 _*_
__author__ = 'Yang Haibo'
__date__ = '2020/5/25 7:26'

from random import choice

from django.contrib.auth import get_user_model
from django.test import TestCase

from core import models


def sample_user(mobile='15257999999', password='123456'):
    """创建一个用户实例"""
    return get_user_model().objects.create_user(mobile, password)


class UserModelTests(TestCase):

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


class TagModelTests(UserModelTests):

    def test_tag_str(self):
        """测试：返回标签对象的字符串表示，成功"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='超人'
        )

        self.assertEqual(str(tag), tag.name)


class SmsCodeModelTests(TestCase):

    def test_create_sms_code_successful(self):
        """测试：创建短信验证码，成功"""
        mobile = '15257999999'
        code = '1234'
        sms_code = models.SmsCode.objects.create(
            mobile=mobile,
            code=code
        )

        self.assertEqual(sms_code.mobile, mobile)
        self.assertEqual(sms_code.code, code)


    def test_sms_code_str(self):
        """测试：返回短信验证码对象的字符串表示，成功"""
        smscode = models.SmsCode.objects.create(
            mobile='15257999999',
            code='123456'
        )

        self.assertEqual(str(smscode), smscode.code)
