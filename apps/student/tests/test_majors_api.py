# _*_ coding: utf-8 _*_
__author__ = 'Yang Haibo'
__date__ = '2020/6/3 7:26'

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import MajorCategory, Major
from student.serializers import MajorSerializer

MAJORS_URL = reverse('student:major-list')


def sample_major_category():
    """创建一个二级专业类别样例，并返回"""
    top_major_category = MajorCategory.objects.create(
        name='一级专业类别名称',
        category_type=1
    )
    major_category = MajorCategory.objects.create(
        name='二级专业类别名称',
        category_type=2,
        parent_category=top_major_category
    )
    return major_category


def create_user(**kwargs):
    """创建一个用户，并返回"""
    return get_user_model().objects.create_user(**kwargs)


class PublicMajorsApiTests(TestCase):
    """测试：专业 API（公共）"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_list_majors_unauthenticated(self):
        """测试：要想获得专业信息列表，用户必须通过验证，否则失败"""
        res = self.client.get(MAJORS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateMajorsApiTests(TestCase):
    """测试：专业 API（私有）"""

    def setUp(self) -> None:
        self.user = create_user(
            mobile='15257911111',
            password='123456',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_majors_successful(self):
        """测试：获取专业信息列表，成功"""
        major_category = sample_major_category()
        Major.objects.create(
            name='专业名称1',
            short_code='A1',
            category=major_category
        )
        Major.objects.create(
            name='专业名称2',
            short_code='A2',
            category=major_category
        )

        res = self.client.get(MAJORS_URL)

        majors = Major.objects.all().order_by('-id')
        serializer = MajorSerializer(majors, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_major_successful(self):
        """测试：创建新的专业，成功"""
        major_category = sample_major_category()
        payload = {
            'name': '专业名称',
            'short_code': 'A1',
            'category': major_category.id
        }

        res = self.client.post(MAJORS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        major = Major.objects.get(id=res.data['id'])
        self.assertEqual(
            major.category_id,
            major_category.id
        )
