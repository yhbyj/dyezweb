# _*_ coding: utf-8 _*_
__author__ = 'Yang Haibo'
__date__ = '2020/6/4 7:56'

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Dormitory
from student.serializers import DormitorySerializer

DORMITORIES_URL = reverse('student:dormitory-list')


def sample_dormitory():
    """创建一个寝室样例，并返回"""
    return Dormitory.objects.create(
        building=7,
        short_code='405'
    )


def create_user(**kwargs):
    """创建一个用户，并返回"""
    return get_user_model().objects.create_user(**kwargs)


class PublicDormitoriesApiTests(TestCase):
    """测试：寝室 API（公共）"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_list_dormitories_unauthenticated(self):
        """测试：要想获得寝室信息列表，用户必须通过验证，否则失败"""
        res = self.client.get(DORMITORIES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateDormitoriesApiTests(TestCase):
    """测试：寝室 API（私有）"""

    def setUp(self) -> None:
        self.user = create_user(
            mobile='15257911111',
            password='123456',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_dormitories_successful(self):
        """测试：获取寝室信息列表，成功"""
        sample_dormitory()
        sample_dormitory()
        res = self.client.get(DORMITORIES_URL)

        dormitories = Dormitory.objects.all().order_by('-id')
        serializer = DormitorySerializer(dormitories, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_dormitory_successful(self):
        """测试：创建新的寝室，成功"""
        payload = {
            'building': 7,
            'short_code': '405'
        }

        res = self.client.post(DORMITORIES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        dormitory = Dormitory.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(dormitory, key))
