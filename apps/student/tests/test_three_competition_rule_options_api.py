# _*_ coding: utf-8 _*_
__author__ = 'Yang Haibo'
__date__ = '2020/6/3 7:26'

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import ThreeCompetitionRuleCategory, \
    ThreeCompetitionRuleOption, ThreeCompetitionRule
from student.serializers import ThreeCompetitionRuleOptionSerializer

THREE_COMPETITION_RULE_OPTIONS_URL = \
    reverse('student:threecompetitionruleoption-list')


def sample_three_competition_rule():
    """创建一个二级三项竞赛评分细则样例，并返回"""
    top_three_competition_rule_category = \
        ThreeCompetitionRuleCategory.objects.create(
            name='一级三项竞赛评分细则选项类别名称',
            category_type=1
        )
    three_competition_rule_category = \
        ThreeCompetitionRuleCategory.objects.create(
            name='二级三项竞赛评分细则选项类别名称',
            category_type=2,
            parent_category=top_three_competition_rule_category
        )
    three_competition_rule = \
        ThreeCompetitionRule.objects.create(
            name='三项竞赛评分细则选项名称',
            code='000001',
            category=three_competition_rule_category
        )
    return three_competition_rule


def create_user(**kwargs):
    """创建一个用户，并返回"""
    return get_user_model().objects.create_user(**kwargs)


class PublicThreeCompetitionRuleOptionsApiTests(TestCase):
    """测试：三项竞赛评分细则选项 API（公共）"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_list_three_competition_rules_unauthenticated(self):
        """测试：要想获得三项竞赛评分细则选项信息列表，用户必须通过验证，否则失败"""
        res = self.client.get(THREE_COMPETITION_RULE_OPTIONS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateThreeCompetitionRuleOptionsApiTests(TestCase):
    """测试：三项竞赛评分细则选项 API（私有）"""

    def setUp(self) -> None:
        self.user = create_user(
            mobile='15257911111',
            password='123456',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_three_competition_rule_options_successful(self):
        """测试：获取三项竞赛评分细则选项信息列表，成功"""
        three_competition_rule = sample_three_competition_rule()
        ThreeCompetitionRuleOption.objects.create(
            name='三项竞赛评分细则选项名称1',
            value='选项值1',
            rule=three_competition_rule
        )
        ThreeCompetitionRuleOption.objects.create(
            name='三项竞赛评分细则选项名称2',
            value='选项值2',
            rule=three_competition_rule
        )

        res = self.client.get(THREE_COMPETITION_RULE_OPTIONS_URL)

        three_competition_rule_options = \
            ThreeCompetitionRuleOption.objects.all().order_by('-id')
        serializer = ThreeCompetitionRuleOptionSerializer(
            three_competition_rule_options,
            many=True
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_three_competition_rule_option_successful(self):
        """测试：创建新的三项竞赛评分细则选项，成功"""
        three_competition_rule = sample_three_competition_rule()
        payload = {
            'name': '三项竞赛评分细则选项名称',
            'value': '选项值',
            'rule': three_competition_rule.id
        }

        res = self.client.post(THREE_COMPETITION_RULE_OPTIONS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        three_competition_rule_option = \
            ThreeCompetitionRuleOption.objects.get(id=res.data['id'])
        self.assertEqual(
            three_competition_rule_option.rule_id,
            three_competition_rule.id
        )
