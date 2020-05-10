from django.db import models

# from tinymce.models import HTMLField
from DjangoUeditor.models import UEditorField

from utils.db.base_model import BaseModel

# Create your models here.


class ServiceCategory(BaseModel):
    """服务类别"""
    # 招生
    name = models.CharField(max_length=10, verbose_name='名称')
    # 空
    parent = models.ForeignKey('self', related_name='subs', null=True, blank=True, on_delete=models.CASCADE,
                               verbose_name='父类别')

    class Meta:
        db_table = 'tb_service_category'
        verbose_name = '服务类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class SPU(BaseModel):
    """服务SPU"""
    # 2020年东阳市职教中心招生
    name = models.CharField(max_length=50, verbose_name='名称')
    # 富文本类型:带有格式的文本
    # 招生简章
    # detail = HTMLField(blank=True, verbose_name='服务详情')
    detail = UEditorField(blank=True, verbose_name='服务详情')

    class Meta:
        db_table = 'tb_spu'
        verbose_name = '服务SPU'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class SPUSpecification(BaseModel):
    """服务SPU规格"""
    # 2020年东阳市职教中心招生（专业填报）
    spu = models.ForeignKey(SPU, on_delete=models.CASCADE, related_name='specs', verbose_name='服务SPU')
    # 校区、专业等
    name = models.CharField(max_length=20, verbose_name='规格名称')

    class Meta:
        db_table = 'tb_spu_specification'
        verbose_name = '服务SPU规格'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s: %s' % (self.spu.name, self.name)


class SpecificationOption(BaseModel):
    """规格选项"""
    # 校区
    spec = models.ForeignKey(SPUSpecification, related_name='options', on_delete=models.CASCADE, verbose_name='规格')
    # 东阳二职、东阳技校等
    value = models.CharField(max_length=20, verbose_name='选项值')

    class Meta:
        db_table = 'tb_specification_option'
        verbose_name = '规格选项'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s - %s' % (self.spec, self.value)

class SKU(BaseModel):
    """服务SKU"""
    # 选择专业：2020年东阳二职校区计算机五年一贯专业
    name = models.CharField(max_length=50, verbose_name='名称')
    # 杭州育英职业技术学院
    caption = models.CharField(max_length=100, verbose_name='副标题')
    # 2020年东阳市职教中心招生（专业填报）
    spu = models.ForeignKey(SPU, on_delete=models.CASCADE, verbose_name='服务')
    # 招生
    category = models.ForeignKey(ServiceCategory, on_delete=models.PROTECT, verbose_name='从属类别')
    # 住宿费等杂费 560元
    fee = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='费用')
    # 名额，例如45
    quotas = models.IntegerField(default=0, verbose_name='名额')
    comments = models.IntegerField(default=0, verbose_name='评价数')
    is_launched = models.BooleanField(default=True, verbose_name='是否上架')
    default_image = models.ImageField(max_length=200, default='', null=True, blank=True, verbose_name='默认图片')

    class Meta:
        db_table = 'tb_sku'
        verbose_name = '服务SKU'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s: %s' % (self.id, self.name)


class SKUImage(BaseModel):
    """服务SKU图片"""
    # 选择专业：2020年东阳二职校区计算机五年一贯专业
    sku = models.ForeignKey(SKU, on_delete=models.CASCADE, verbose_name='sku')
    # 有许多宣传的照片
    image = models.ImageField(verbose_name='图片')

    class Meta:
        db_table = 'tb_sku_image'
        verbose_name = 'SKU图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s %s' % (self.sku.name, self.id)


class SKUSpecification(BaseModel):
    """SKU具体规格"""
    # 选择专业：2020年东阳二职校区计算机五年一贯专业
    sku = models.ForeignKey(SKU, related_name='specs', on_delete=models.CASCADE, verbose_name='sku')
    # 校区、专业等
    spec = models.ForeignKey(SPUSpecification, on_delete=models.PROTECT, verbose_name='规格名称')
    # 东阳二职、计算机五年一贯
    option = models.ForeignKey(SpecificationOption, on_delete=models.PROTECT, verbose_name='规格值')

    class Meta:
        db_table = 'tb_sku_specification'
        verbose_name = '服务SKU规格'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '%s: %s - %s' % (self.sku, self.spec.name, self.option.value)
