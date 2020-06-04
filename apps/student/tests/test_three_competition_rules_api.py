# _*_ coding: utf-8 _*_
__author__ = 'Yang Haibo'
__date__ = '2020/6/3 7:26'

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import ThreeCompetitionRuleCategory, ThreeCompetitionRule
from student.serializers import ThreeCompetitionRuleSerializer

THREE_COMPETITION_RULES_URL = reverse('student:threecompetitionrule-list')


def sample_three_competition_rule_category():
    """创建一个二级三项竞赛评分细则类别样例，并返回"""
    top_three_competition_rule_category = \
        ThreeCompetitionRuleCategory.objects.create(
            name='一级三项竞赛评分细则类别名称',
            category_type=1
        )
    three_competition_rule_category = \
        ThreeCompetitionRuleCategory.objects.create(
            name='二级三项竞赛评分细则类别名称',
            category_type=2,
            parent_category=top_three_competition_rule_category
        )
    return three_competition_rule_category


def create_user(**kwargs):
    """创建一个用户，并返回"""
    return get_user_model().objects.create_user(**kwargs)


class PublicThreeCompetitionRulesApiTests(TestCase):
    """测试：三项竞赛评分细则 API（公共）"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_list_three_competition_rules_unauthenticated(self):
        """测试：要想获得三项竞赛评分细则信息列表，用户必须通过验证，否则失败"""
        res = self.client.get(THREE_COMPETITION_RULES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateThreeCompetitionRulesApiTests(TestCase):
    """测试：三项竞赛评分细则 API（私有）"""

    def setUp(self) -> None:
        self.user = create_user(
            mobile='15257911111',
            password='123456',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_three_competition_rules_successful(self):
        """测试：获取三项竞赛评分细则信息列表，成功"""
        three_competition_rule_category = \
            sample_three_competition_rule_category()
        ThreeCompetitionRule.objects.create(
            name='三项竞赛评分细则名称1',
            code='000001',
            category=three_competition_rule_category
        )
        ThreeCompetitionRule.objects.create(
            name='三项竞赛评分细则名称2',
            code='000002',
            category=three_competition_rule_category
        )

        res = self.client.get(THREE_COMPETITION_RULES_URL)

        three_competition_rules = \
            ThreeCompetitionRule.objects.all().order_by('-id')
        serializer = ThreeCompetitionRuleSerializer(
            three_competition_rules,
            many=True
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_three_competition_rule_successful(self):
        """测试：创建新的三项竞赛评分细则，成功"""
        three_competition_rule_category = \
            sample_three_competition_rule_category()
        payload = {
            'name': '三项竞赛评分细则名称',
            'code': '000001',
            'category': three_competition_rule_category.id
        }

        res = self.client.post(THREE_COMPETITION_RULES_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        three_competition_rule = \
            ThreeCompetitionRule.objects.get(id=res.data['id'])
        self.assertEqual(
            three_competition_rule.category_id,
            three_competition_rule_category.id
        )
