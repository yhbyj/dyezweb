from django.db import models
from utils.db.base_model import BaseModel


# Create your models here.
class MajorCategory(BaseModel):
    """
    专业类别模型类
    """
    CATEGORY_TYPE = (
        (1, "一级类别"),
        (2, "二级类别"),
    )
    name = models.CharField(max_length=50, verbose_name='专业类别')
    desc = models.TextField(default="", verbose_name="类别描述")
    # 设置目录树的级别
    category_type = models.IntegerField(choices=CATEGORY_TYPE, verbose_name="类别级别")
    # 设置models有一个指向自己的外键
    parent_category = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, verbose_name="父类别",
                                        related_name="sub_cat")
    is_tab = models.BooleanField(default=False, verbose_name="是否导航", help_text="是否导航")

    class Meta:
        db_table = 'tb_major_category'
        verbose_name = "专业类别"
        verbose_name_plural = verbose_name

    def __str__(self):
        title = '{}--{}'.format(self.parent_category, self.name)
        title = title.replace('None--', '')
        return title


class Major(BaseModel):
    """
    专业模型类
    """
    status_choices = (
        (0, '下线'),
        (1, '上线'),
    )
    category = models.ForeignKey(MajorCategory, on_delete=models.CASCADE, verbose_name="专业类别")
    code = models.CharField(max_length=2, verbose_name="专业编号")
    name = models.CharField(max_length=50, verbose_name='专业名称')
    status = models.SmallIntegerField(default=1, choices=status_choices, verbose_name='专业状态')

    class Meta:
        db_table = 'tb_major'
        verbose_name = "专业"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name