from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from utils.db.base_model import BaseModel


# 模型已经迁移建表,并且表中已经有数据之后,再给表/模型新增字段时,必须给默认值或可以为空,不然迁移就报错
class Account(AbstractUser):
    """
    账户模型类（自定义用户模型类）
    """
    # 如果手机号唯一，一个手机号对应一个用户，多个用户无法共享一个手机号。
    # 如何解决一户有多个小孩报名？
    # mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号码')
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name='手机号码')
    # 原有用户模型已经有邮箱字段，但是没有邮箱验证状态。
    email_active = models.BooleanField(default=False, verbose_name='邮箱验证状态')

    class Meta:
        db_table = 'tb_account'
        verbose_name = '账户'
        verbose_name_plural = verbose_name

    def __str__(self):
        # 返回原有用户模型的用户名
        return self.username


