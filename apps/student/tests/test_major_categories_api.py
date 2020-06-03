# _*_ coding: utf-8 _*_
__author__ = 'Yang Haibo'
__date__ = '2020/6/3 7:26'

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import MajorCategory
from student.serializers import MajorCategorySerializer

MAJOR_CATEGORIES_URL = reverse('student:majorcategory-list')


def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


class PublicMajorCategoriesApiTests(TestCase):
    """测试：专业类别 API（公共）"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_list_major_categories_unauthenticated(self):
        """测试：要想获得专业类别信息列表，用户必须通过验证，否则失败"""
        res = self.client.get(MAJOR_CATEGORIES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateMajorCategoriesApiTests(TestCase):
    """测试：专业类别 API（私有）"""

    def setUp(self) -> None:
        self.user = create_user(
            mobile='15257911111',
            password='123456',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_major_categories_successful(self):
        """测试：获取专业类别信息列表，成功"""
        top_major_category1 = MajorCategory.objects.create(
            name='一级专业类别名称1',
            category_type=1
        )
        MajorCategory.objects.create(
            name='二级专业类别名称1',
            category_type=2,
            parent_category=top_major_category1
        )
        top_major_category2 = MajorCategory.objects.create(
            name='一级专业类别名称2',
            category_type=1
        )
        MajorCategory.objects.create(
            name='二级专业类别名称2',
            category_type=2,
            parent_category=top_major_category2
        )

        res = self.client.get(MAJOR_CATEGORIES_URL)

        major_categories = MajorCategory.objects.filter(
            category_type=1
        ).order_by('-id')
        serializer = MajorCategorySerializer(major_categories, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_major_category_successful(self):
        """测试：创建新的专业类别，成功"""
        top_major_category = MajorCategory.objects.create(
            name='一级专业类别名称',
            category_type=1
        )
        payload = {
            'name': '二级专业类别名称',
            'category_type': 2,
            'parent_category': top_major_category.id
        }

        res = self.client.post(MAJOR_CATEGORIES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        major_category = MajorCategory.objects.get(id=res.data['id'])
        self.assertEqual(
            major_category.parent_category_id,
            top_major_category.id
        )
