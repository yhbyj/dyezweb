from django.db import models

# Create your models here.
from dorms.models import Dormitory
from utils.db.base_model import BaseModel


class ThreeCompetitionRuleCategory(BaseModel):
    """
    三项竞赛评分细则类别模型类
    """
    CATEGORY_TYPE = (
        (1, "一级类别"),
        (2, "二级类别"),
    )
    name = models.CharField(max_length=50, verbose_name='三项竞赛评分细则类别')
    desc = models.TextField(null=True, blank=True, verbose_name="类别描述")
    # 设置目录树的级别
    category_type = models.SmallIntegerField(default=2, choices=CATEGORY_TYPE, verbose_name="类别级别")
    # 设置models有一个指向自己的外键
    parent_category = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, verbose_name="父类别",
                                        related_name="sub_cat")

    class Meta:
        db_table = 'tb_three_competition_rule_category'
        verbose_name = "三项竞赛评分细则类别"
        verbose_name_plural = verbose_name

    def __str__(self):
        title = '{}--{}'.format(self.parent_category, self.name)
        title = title.replace('None--', '')
        return title


class ThreeCompetitionRule(BaseModel):
    """
    三项竞赛评分细则模型类
    """
    # 三项竞赛评分细则对应的类别应该是二级类别，不能对应一级类别，如何解决？
    category = models.ForeignKey(ThreeCompetitionRuleCategory, on_delete=models.CASCADE, verbose_name="三项竞赛评分细则类别")
    name = models.CharField(max_length=50, verbose_name='三项竞赛评分细则名称')
    code = models.CharField(max_length=6, null=True, blank=True, verbose_name="三项竞赛评分细则代码")
    desc = models.TextField(null=True, blank=True, verbose_name="三项竞赛评分细则描述")
    min = models.DecimalField(default=0.00, max_digits=3, decimal_places=2,  verbose_name='评分区间下限')
    max = models.DecimalField(default=5.00, max_digits=3, decimal_places=2, verbose_name='评分区间上限')

    class Meta:
        db_table = 'tb_three_competition_rule'
        verbose_name = '三项竞赛评分细则'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class ThreeCompetitionRuleOption(BaseModel):
    """
    三项竞赛评分细则选项模型类
    """
    rule = models.ForeignKey(ThreeCompetitionRule, on_delete=models.CASCADE, verbose_name="三项竞赛评分细则")
    name = models.CharField(max_length=50, verbose_name='选项名称')
    value = models.CharField(max_length=50, verbose_name='选项值')

    class Meta:
        db_table = 'tb_three_competition_rule_option'
        verbose_name = '三项竞赛评分细则选项'
        verbose_name_plural = verbose_name

    def __str__(self):
        title = '{}--{}--{}'.format(self.rule, self.name, self.value)
        title = title.replace('None--', '')
        return title


class ThreeCompetition(BaseModel):
    """
    三项竞赛模型类
    """
    option = models.ForeignKey(ThreeCompetitionRuleOption, on_delete=models.CASCADE, verbose_name="三项竞赛评分细则选项")
    score = models.DecimalField(default=0.00, max_digits=3, decimal_places=2, verbose_name='评分')
    is_minus = models.BooleanField(default=True, verbose_name='是否扣分')

    class Meta:
        db_table = 'tb_three_competition'
        verbose_name = '三项竞赛'
        verbose_name_plural = verbose_name

    def __str__(self):
        title = '{}'.format(self.option)
        title = title.replace('None', '')
        return title

class DormitoryCompetition(BaseModel):
    """
    寝室竞赛模型类
    """
    dormitory = models.ForeignKey(Dormitory, on_delete=models.CASCADE, verbose_name="寝室")
    option = models.ForeignKey(ThreeCompetitionRuleOption, on_delete=models.CASCADE, verbose_name="三项竞赛评分细则选项")
    score = models.DecimalField(default=0.00, max_digits=3, decimal_places=2, verbose_name='评分')
    is_minus = models.BooleanField(default=True, verbose_name='是否扣分')

    class Meta:
        db_table = 'tb_three_competition_dormitory'
        verbose_name = '寝室竞赛'
        verbose_name_plural = verbose_name

    def __str__(self):
        title = '{}--{}'.format(self.dormitory,self.option)
        title = title.replace('None--', '')
        return title