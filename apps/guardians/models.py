from django.db import models

from utils.db.base_model import BaseModel

# Create your models here.


class Guardian(BaseModel):
    """
    监护人模型类
    """
    name = models.CharField(max_length=50, verbose_name='姓名')

    class Meta:
        db_table = 'tb_guardian'
        verbose_name = '监护人'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class GuardianAddress(BaseModel):
    """
    监护人地址模型类
    """
    guardian = models.ForeignKey(Guardian, on_delete=models.CASCADE, related_name='addresses', verbose_name='监护人')
    title = models.CharField(max_length=20, verbose_name='地址名称')
    province = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='province_addresses',
                                 verbose_name='省')
    city = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='city_addresses', verbose_name='市')
    district = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='district_addresses',
                                 verbose_name='区')
    place = models.CharField(max_length=50, verbose_name='地址')
    mobile = models.CharField(max_length=11, verbose_name='手机')
    tel = models.CharField(max_length=20, null=True, blank=True, default='', verbose_name='固定电话')
    email = models.CharField(max_length=30, null=True, blank=True, default='', verbose_name='电子邮箱')
    # 邮政编码
    zip_code = models.CharField(max_length=6, verbose_name='邮政编码')

    class Meta:
        db_table = 'tb_guardian_address'
        verbose_name = '监护人地址'
        verbose_name_plural = verbose_name
        ordering = ['-update_time']