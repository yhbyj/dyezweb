# _*_ coding: utf-8 _*_
__author__ = 'Yang Haibo'
__date__ = '2020/5/26 17:36'

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Tag
from recipe.serializers import TagSerializer


TAGS_URL = reverse('recipe:tag-list')


def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


class PublicTagApiTests(TestCase):
    """测试：不需要验证就能访问的标签 API（公众），不存在"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """测试：用户没有登录，获取标签列表，失败"""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagApiTests(TestCase):
    """测试：需要验证后，才能访问的标签 API（私有）"""

    def setUp(self) -> None:
        self.user = create_user(
            mobile='15257999999',
            password='123456',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_tags(self):
        """测试：已登录用户，获取标签列表，成功"""
        Tag.objects.create(user=self.user, name='超人')
        Tag.objects.create(user=self.user, name='IT')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """测试：只能获取用户自己的标签"""
        user2 = create_user(
            mobile='15257911111',
            password='123456',
        )
        Tag.objects.create(user=user2, name='蝙蝠侠')
        tag = Tag.objects.create(user=self.user, name='超人')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # self.assertEqual(res.data[0]['name'], tag.name)
        # self.assertEqual(len(res.data), 1)

    def test_create_tag_successful(self):
        """测试：通过验证后，创建标签信息，成功"""
        payload = {'name': '测试标签'}

        res = self.client.post(TAGS_URL, payload)

        exists = Tag.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()

        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """测试：通过无效负载创建标签，失败"""
        payload = {'name': ''}

        res = self.client.post(TAGS_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

