from django.db import models

# Create your models here.


class Area(models.Model):
    """省市区"""
    name = models.CharField(max_length=20, verbose_name='名称')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL,
                               related_name='subs',
                               null=True, blank=True,
                               verbose_name='上级行政区划')

    class Meta:
        # 数据表名不是'tb_area'的原因，提供的数据中，表名是'tb_areas'
        db_table = 'tb_areas'
        verbose_name = '省市区'
        verbose_name_plural = '省市区'

    def __str__(self):
        return self.name
