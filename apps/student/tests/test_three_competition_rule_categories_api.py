# _*_ coding: utf-8 _*_
__author__ = 'Yang Haibo'
__date__ = '2020/6/3 7:26'

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import ThreeCompetitionRuleCategory
from student.serializers import ThreeCompetitionRuleCategorySerializer

THREE_COMPETITION_RULE_CATEGORIES_URL = \
    reverse('student:threecompetitionrulecategory-list')


def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


class PublicThreeCompetitionRuleCategoriesApiTests(TestCase):
    """测试：三项竞赛评分细则类别类别 API（公共）"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_list_tcr_categories_unauthenticated(self):
        """测试：要想获得三项竞赛评分细则类别类别信息列表，用户必须通过验证，否则失败"""
        res = self.client.get(THREE_COMPETITION_RULE_CATEGORIES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateThreeCompetitionRuleCategoriesApiTests(TestCase):
    """测试：三项竞赛评分细则类别类别 API（私有）"""

    def setUp(self) -> None:
        self.user = create_user(
            mobile='15257911111',
            password='123456',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_tcr_categories_successful(self):
        """测试：获取三项竞赛评分细则类别类别信息列表，成功"""
        top_three_competition_rule_category1 = \
            ThreeCompetitionRuleCategory.objects.create(
                name='一级三项竞赛评分细则类别类别名称1',
                category_type=1
            )
        ThreeCompetitionRuleCategory.objects.create(
            name='二级三项竞赛评分细则类别类别名称1',
            category_type=2,
            parent_category=top_three_competition_rule_category1
        )
        top_three_competition_rule_category2 = \
            ThreeCompetitionRuleCategory.objects.create(
                name='一级三项竞赛评分细则类别类别名称2',
                category_type=1
            )
        ThreeCompetitionRuleCategory.objects.create(
            name='二级三项竞赛评分细则类别类别名称2',
            category_type=2,
            parent_category=top_three_competition_rule_category2
        )

        res = self.client.get(THREE_COMPETITION_RULE_CATEGORIES_URL)

        three_competition_rule_categories = \
            ThreeCompetitionRuleCategory.objects.filter(
                category_type=1
            ).order_by('-id')
        serializer = ThreeCompetitionRuleCategorySerializer(
            three_competition_rule_categories,
            many=True
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_tcr_category_successful(self):
        """测试：创建新的三项竞赛评分细则类别类别，成功"""
        top_three_competition_rule_category = \
            ThreeCompetitionRuleCategory.objects.create(
                name='一级三项竞赛评分细则类别类别名称',
                category_type=1
            )
        payload = {
            'name': '二级三项竞赛评分细则类别类别名称',
            'category_type': 2,
            'parent_category': top_three_competition_rule_category.id
        }

        res = self.client.post(
            THREE_COMPETITION_RULE_CATEGORIES_URL,
            payload
        )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        three_competition_rule_category = \
            ThreeCompetitionRuleCategory.objects.get(id=res.data['id'])
        self.assertEqual(
            three_competition_rule_category.parent_category_id,
            top_three_competition_rule_category.id
        )
