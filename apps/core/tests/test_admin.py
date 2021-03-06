# _*_ coding: utf-8 _*_
__author__ = 'Yang Haibo'
__date__ = '2020/5/25 9:18'

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from core.models import Admission


class AdminSiteTests(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            mobile='15257999999',
            password='123456'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            mobile='15257911111',
            password='123456',
            name='测试用户全名'
        )
        self.admission = Admission.objects.create(
            user=self.admin_user,
            name='入学报名学生',
            parent_name='家长'
        )

    def test_users_listed(self):
        """测试：用户出现在用户列表页"""
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.mobile)

    def test_user_change_page(self):
        """测试：编辑用户页正常"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """测试：创建用户页正常"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_admissions_listed(self):
        """测试：入学报名出现在入学报名列表页"""
        url = reverse('admin:core_admission_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.admission.name)
        self.assertContains(res, self.admission.parent_name)

    def test_admission_change_page(self):
        """测试：编辑入学报名页正常"""
        url = reverse('admin:core_admission_change', args=[self.admission.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_admission_page(self):
        """测试：创建入学报名页正常"""
        url = reverse('admin:core_admission_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
