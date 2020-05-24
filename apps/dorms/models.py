from django.db import models

# Create your models here.
from utils.db.base_model import BaseModel


class Dormitory(BaseModel):
    """
    学生宿舍模型类
    """
    building_choices = (
        (6, '6号楼'),
        (7, '7号楼'),
        (8, '8号楼'),
    )
    # 寝室编号，必填项，如405
    short_code = models.CharField(max_length=3, verbose_name="寝室编号")
    # 学生自己起的名字，非必填项
    name = models.CharField(max_length=50, null=True, blank=True, verbose_name='寝室名称')
    beds = models.SmallIntegerField(default=10, verbose_name='床位数')
    with_bathroom = models.BooleanField(default=True, verbose_name='是否带卫生间')
    building = models.SmallIntegerField(default=7, choices=building_choices, verbose_name='所属楼栋')

    class Meta:
        db_table = 'tb_dormitory'
        verbose_name = '寝室'
        verbose_name_plural = verbose_name

    def __str__(self):
        title = '{}-{}'.format(self.building, self.short_code)
        title = title.replace('None-', '')
        return title