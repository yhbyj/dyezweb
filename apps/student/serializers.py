# _*_ coding: utf-8 _*_
__author__ = 'Yang Haibo'
__date__ = '2020/6/1 16:08'

from rest_framework import serializers

from core import models


class MajorCategorySerializer2(serializers.ModelSerializer):
    """一级专业类别对象序列化"""

    class Meta:
        model = models.MajorCategory
        fields = ('id', 'name', )
        read_only_fields = ('id', 'name', )


class MajorCategorySerializer(serializers.ModelSerializer):
    """一级专业类别对象序列化"""
    sub_cat = MajorCategorySerializer2

    class Meta:
        model = models.MajorCategory
        fields = ('id', 'name', 'category_type', 'parent_category', 'sub_cat')
        read_only_fields = ('id', 'sub_cat')


class MajorSerializer(serializers.ModelSerializer):
    """专业对象序列化"""

    class Meta:
        model = models.Major
        fields = ('id', 'name', 'short_code', 'category')
        read_only_fields = ('id',)


class AdmissionSerializer(serializers.ModelSerializer):
    """入学报名对象序列化"""
    majors = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=models.Major.objects.all()
    )

    class Meta:
        model = models.Admission
        exclude = ('user', 'create_time', 'update_time', 'is_delete', )
        read_only_fields = ('id', )


class AdmissionDetailSerializer(AdmissionSerializer):
    """入学报名详情对象序列化"""
    majors = MajorSerializer(many=True, read_only=True)


class DormitorySerializer(serializers.ModelSerializer):
    """入学报名对象序列化"""

    class Meta:
        model = models.Dormitory
        exclude = ('create_time', 'update_time', 'is_delete', )
        read_only_fields = ('id', )


class ThreeCompetitionRuleCategorySerializer2(serializers.ModelSerializer):
    """一级三项竞赛评分细则类别对象序列化"""

    class Meta:
        model = models.ThreeCompetitionRuleCategory
        fields = ('id', 'name', )
        read_only_fields = ('id', 'name', )


class ThreeCompetitionRuleCategorySerializer(serializers.ModelSerializer):
    """一级三项竞赛评分细则类别对象序列化"""
    sub_cat = ThreeCompetitionRuleCategorySerializer2

    class Meta:
        model = models.ThreeCompetitionRuleCategory
        fields = ('id', 'name', 'category_type', 'parent_category', 'sub_cat')
        read_only_fields = ('id', 'sub_cat')


class ThreeCompetitionRuleSerializer(serializers.ModelSerializer):
    """三项竞赛评分细则对象序列化"""

    class Meta:
        model = models.ThreeCompetitionRule
        fields = ('id', 'name', 'code', 'category')
        read_only_fields = ('id',)


class ThreeCompetitionRuleOptionSerializer(serializers.ModelSerializer):
    """三项竞赛评分细则选项对象序列化"""

    class Meta:
        model = models.ThreeCompetitionRuleOption
        fields = ('id', 'name', 'value', 'rule')
        read_only_fields = ('id',)


class DormitoryCompetitionSerializer(serializers.ModelSerializer):
    """入学寝室竞赛对象序列化"""

    class Meta:
        model = models.DormitoryCompetition
        fields = ('id', 'dormitory', 'option', 'score')
        read_only_fields = ('id',)
