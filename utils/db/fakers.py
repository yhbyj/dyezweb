# _*_ coding: utf-8 _*_
__author__ = 'Yang Haibo'
__date__ = '2020/5/10 17:41'

import os
import sys

import django
from faker import Faker
from django.utils import timezone

# 将项目根目录添加到 Python 的模块搜索路径中
back = os.path.dirname
BASE_DIR = back(back(back(back(os.path.abspath(__file__)))))
sys.path.append(BASE_DIR)

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dyezweb.settings.local")
    django.setup()

    from accounts.models import Account

    print('clean database')
    Account.objects.all().delete()
    print('create a super user account')
    account = Account.objects.create_superuser('admin', 'admin@dyez.com', 'admin')
    print('create some faked accounts joined within the past year')
    myfaker = Faker('zh_CN')
    # 创建速度很慢，并且在创建100个时，在username字段上曾出现违反unique constraints
    for _ in range(25):
        joined_time = myfaker.date_time_between(start_date='-1y', end_date="now",
                                                tzinfo=timezone.get_current_timezone())
        account = Account.objects.create_user(username=myfaker.user_name(),
                                              email=myfaker.email(),
                                              password='123',
                                              is_staff=False,
                                              date_joined=joined_time)
        account.save()