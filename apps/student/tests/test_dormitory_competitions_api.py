# _*_ coding: utf-8 _*_
__author__ = 'Yang Haibo'
__date__ = '2020/6/1 15:59'

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import ThreeCompetitionRuleCategory, \
    Dormitory, ThreeCompetitionRule, ThreeCompetitionRuleOption, \
    DormitoryCompetition
from student.serializers import DormitoryCompetitionSerializer

DORMITORY_COMPETITIONS_URL = reverse('student:dormitorycompetition-list')


def sample_three_competition_rule_option():
    """创建一个二级三项竞赛评分细则选项样例，并返回"""
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
    three_competition_rule_option = \
        ThreeCompetitionRuleOption.objects.create(
            name='三项竞赛评分细则选项名称',
            value='选项值',
            rule=three_competition_rule
        )
    return three_competition_rule_option


def sample_dormitory():
    """创建一个寝室样例，并返回"""
    return Dormitory.objects.create(
        building=7,
        short_code='405'
    )


def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


class PublicDormitoryCompetitionsApiTests(TestCase):
    """测试：寝室竞赛 API（公共）"""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_list_dormitory_competitions_unauthenticated(self):
        """测试：要想获得寝室竞赛信息列表，用户必须通过验证，否则失败"""
        res = self.client.get(DORMITORY_COMPETITIONS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateDormitoryCompetitionsApiTests(TestCase):
    """测试：寝室竞赛 API（私有）"""

    def setUp(self) -> None:
        self.user = create_user(
            mobile='15257911111',
            password='123456',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_dormitory_competitions_successful(self):
        """测试：获得寝室竞赛信息列表，成功"""
        three_competition_rule_option = \
            sample_three_competition_rule_option()
        dormitory = sample_dormitory()
        DormitoryCompetition.objects.create(
            option=three_competition_rule_option,
            dormitory=dormitory,
            score=0.25
        )
        DormitoryCompetition.objects.create(
            option=three_competition_rule_option,
            dormitory=dormitory,
            score=0.5
        )

        res = self.client.get(DORMITORY_COMPETITIONS_URL)

        dormitory_competitions = \
            DormitoryCompetition.objects.all().order_by('-id')
        serializer = DormitoryCompetitionSerializer(
            dormitory_competitions,
            many=True
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_dormitory_competition_successful(self):
        """测试：创建寝室竞赛，成功"""
        three_competition_rule_option = \
            sample_three_competition_rule_option()
        dormitory = sample_dormitory()
        payload = {
            'option': three_competition_rule_option.id,
            'dormitory': dormitory.id,
            'score': 0.25
        }

        res = self.client.post(DORMITORY_COMPETITIONS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
