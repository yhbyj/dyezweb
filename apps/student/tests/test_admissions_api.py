# _*_ coding: utf-8 _*_
__author__ = 'Yang Haibo'
__date__ = '2020/6/1 15:59'

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Admission, Major, MajorCategory
from student.serializers import AdmissionSerializer, AdmissionDetailSerializer

ADMISSIONS_URL = reverse('student:admission-list')


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


def sample_major(category=None):
    """创建一个二级类别专业样例，并返回"""
    if category is None:
        category = sample_major_category()
    return Major.objects.create(
        name='二级类别专业',
        category=category
    )


def detail_url(admission_id):
    """返回入学报名详细信息的url地址"""
    return reverse('student:admission-detail', args=[admission_id])


def sample_admission(user, **kwargs):
    """创建并返回一个入学报名样例对象"""
    defaults = {
        'name': '初中毕业生',
        'id_card_no': '330783200608310001',
        'parent_name': '学生家长'
    }
    defaults.update(kwargs)
    return Admission.objects.create(user=user, **defaults)


def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


class PublicAdmissionsApiTests(TestCase):
    """测试：入学报名 API（公共）"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_list_admissions_unauthenticated(self):
        """测试：要想获得入学报名信息列表，用户必须通过验证，否则失败"""
        res = self.client.get(ADMISSIONS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAdmissionsApiTests(TestCase):
    """测试：入学报名 API（私有）"""

    def setUp(self) -> None:
        self.user = create_user(
            mobile='15257911111',
            password='123456',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_admissions_successful(self):
        """测试：获得入学报名信息列表，成功"""
        sample_admission(user=self.user)
        sample_admission(user=self.user)

        res = self.client.get(ADMISSIONS_URL)

        recipes = Admission.objects.all().order_by('-id')
        serializer = AdmissionSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_list_admissions_limited_to_user(self):
        """测试：只能获得用户自己的入学报名信息列表"""
        user2 = get_user_model().objects.create_user(
            '15257922222',
            '123456'
        )
        sample_admission(user=user2)
        sample_admission(user=self.user)

        res = self.client.get(ADMISSIONS_URL)

        recipes = Admission.objects.filter(user=self.user)
        serializer = AdmissionSerializer(recipes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_admission_detail(self):
        """测试：查看入学报名的详细信息"""
        admission = sample_admission(self.user)
        admission.majors.add(sample_major())
        serializer = AdmissionDetailSerializer(admission)

        url = detail_url(admission.id)
        res = self.client.get(url)

        self.assertEqual(res.data, serializer.data)

    def test_create_admission_successful(self):
        """测试：创建入学申请，成功"""
        payload = {
            'name': '初中毕业生',
            'id_card_no': '330783200608310001',
            'parent_name': '学生家长'
        }

        res = self.client.post(ADMISSIONS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        admission = Admission.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(admission, key))

    def test_create_admission_with_majors(self):
        """测试：创建带专业的入学申请"""
        major_category = sample_major_category()
        major1 = Major.objects.create(
            name='专业名称1',
            short_code='A1',
            category=major_category
        )
        major2 = Major.objects.create(
            name='专业名称2',
            short_code='A2',
            category=major_category
        )
        payload = {
            'name': '初中毕业生',
            'id_card_no': '330783200608310001',
            'parent_name': '学生家长',
            'majors': [major1.id, major2.id]
        }

        res = self.client.post(ADMISSIONS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        admission = Admission.objects.get(id=res.data['id'])
        majors = admission.majors.all()
        self.assertEqual(majors.count(), 2)
        self.assertIn(major1, majors)
        self.assertIn(major2, majors)

    def test_partial_update_admission(self):
        """测试：部分更新入学申请"""
        major_category = sample_major_category()
        major = Major.objects.create(
            name='专业名称1',
            short_code='A1',
            category=major_category
        )
        new_major = Major.objects.create(
            name='专业名称2',
            short_code='A2',
            category=major_category
        )
        admission = sample_admission(self.user)
        admission.majors.add(major)

        payload = {
            'name': '新初中毕业生',
            'majors': [new_major.id]
        }
        url = detail_url(admission.id)
        self.client.patch(url, payload)

        admission.refresh_from_db()
        self.assertEqual(admission.name, payload['name'])
        majors = admission.majors.all()
        self.assertEqual(majors.count(), 1)
        self.assertIn(new_major, majors)

    def test_full_update_admission(self):
        """测试：全部更新入学申请"""
        major_category = sample_major_category()
        major = Major.objects.create(
            name='专业名称1',
            short_code='A1',
            category=major_category
        )
        admission = sample_admission(self.user)
        admission.majors.add(major)

        payload = {
            'name': '新初中毕业生',
            'id_card_no': '33078320060831000X',
            'parent_name': '新学生家长'
        }
        url = detail_url(admission.id)
        self.client.put(url, payload)

        admission.refresh_from_db()
        self.assertEqual(admission.name, payload['name'])
        self.assertEqual(admission.id_card_no, payload['id_card_no'])
        self.assertEqual(admission.parent_name, payload['parent_name'])
        majors = admission.majors.all()
        self.assertEqual(len(majors), 0)

    def test_filter_admission_with_tags(self):
        """测试：根据专业筛选出入学申请"""
        admission1 = sample_admission(user=self.user, name='初中毕业生1')
        admission2 = sample_admission(user=self.user, name='初中毕业生2')
        admission3 = sample_admission(user=self.user, name='初中毕业生3')
        major_category = sample_major_category()
        major1 = Major.objects.create(
            name='专业名称1',
            short_code='A1',
            category=major_category
        )
        major2 = Major.objects.create(
            name='专业名称2',
            short_code='A2',
            category=major_category
        )
        admission1.majors.add(major1)
        admission2.majors.add(major2)

        res = self.client.get(
            ADMISSIONS_URL,
            {'majors': f'{major1.id},{major2.id}'}
        )

        serializer1 = AdmissionSerializer(admission1)
        serializer2 = AdmissionSerializer(admission2)
        serializer3 = AdmissionSerializer(admission3)
        self.assertIn(serializer1.data, res.data)
        self.assertIn(serializer2.data, res.data)
        self.assertNotIn(serializer3.data, res.data)
