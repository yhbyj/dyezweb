from datetime import datetime

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

# Create your models here.


class UserManager(BaseUserManager):
    """自定义用户模型管理类"""

    def create_user(self, mobile, password=None, **extra_fields):
        """创建和保存一个新用户"""
        if not mobile:
            raise ValueError('用户必须有一个有效的手机号码')
        user = self.model(mobile=mobile, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, mobile, password):
        """创建一个超级用户"""
        user = self.create_user(mobile, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


# 模型已经迁移建表,并且表中已经有数据之后,再给表/模型新增字段时,必须给默认值或可以为空,不然迁移就报错
class User(AbstractBaseUser, PermissionsMixin):
    """自定义用户模型，支持手机号"""
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号码')
    name = models.CharField(max_length=255, verbose_name='姓名')
    is_active = models.BooleanField(default=True, verbose_name='激活状态')
    is_staff = models.BooleanField(default=False, verbose_name='员工状态')
    # 原有用户模型已经有邮箱字段，但是没有邮箱验证状态。
    email_active = models.BooleanField(default=False, verbose_name='邮箱验证状态')
    mobile_active = models.BooleanField(default=False, verbose_name='手机验证状态')

    USERNAME_FIELD = 'mobile'

    objects = UserManager()

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class SmsCode(models.Model):
    """
    短信验证码类
    """
    mobile = models.CharField(max_length=11, verbose_name='手机号码')
    code = models.CharField(max_length=10, verbose_name='短信验证码')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = '短信验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code
