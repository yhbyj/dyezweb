from django.db import models

# Create your models here.


class Area(models.Model):
    """
    行政区划类：省市区三级分类，扩展为五级分类，添加层级字段
    """
    AREA_TYPE = (
        (1, "省级（省、自治区、直辖市、特别行政区）"),  # 合计34个省级行政区
        (2, "地级（地级市、地区、自治州、盟）"),   # 合计333个地级区划
        (3, "县级（市辖区、县级市、县、自治县、旗、自治旗、特区、林区）"),  # 合计2846个县级区划
        (4, "乡级（街道、镇、乡、民族乡、苏木、民族苏木、县辖区）"),  # 合计38734个乡级区划
        (5, "村"),
    )
    name = models.CharField(max_length=20, verbose_name='名称')
    # 设置行政区划的级别
    # area_type = models.IntegerField(choices=AREA_TYPE, verbose_name="行政区划级别", help_text="行政区划级别")
    # 设置models有一个指向自己的外键
    parent = models.ForeignKey('self', on_delete=models.SET_NULL,
                               related_name='subs',
                               null=True, blank=True,
                               verbose_name='上级行政区划')

    class Meta:
        # 数据表名不是'tb_area'的原因，提供的数据中，表名是'tb_areas'
        db_table = 'tb_areas'
        # db_table = 'tb_area'
        verbose_name = '行政区划'
        verbose_name_plural = '行政区划'

    def __str__(self):
        return self.name
