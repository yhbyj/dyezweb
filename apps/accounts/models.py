from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from utils.db.base_model import BaseModel


# 模型已经迁移建表,并且表中已经有数据之后,再给表/模型新增字段时,必须给默认值或可以为空,不然迁移就报错
class Account(AbstractUser):
    """
    账户模型类（自定义用户模型类）
    """
    # 账户的手机号是可以为空的（用户注册时，可能没有提供手机号）。
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name='手机号码')
    # 原有用户模型已经有邮箱字段，但是没有邮箱验证状态。
    email_active = models.BooleanField(default=False, verbose_name='邮箱验证状态')

    class Meta:
        db_table = 'tb_account'
        verbose_name = '用户账户'
        verbose_name_plural = verbose_name

    def __str__(self):
        # 返回原有用户模型的用户名
        return self.username


class SmsCode(models.Model):
    """
    短信验证码类
    """
    mobile = models.CharField(max_length=11, verbose_name='手机号码')
    code = models.CharField(max_length=10, verbose_name='短信验证码')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        db_table = 'tb_sms_code'
        verbose_name = '短信验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code