# _*_ coding: utf-8 _*_
__author__ = 'Yang Haibo'
__date__ = '2020/4/29 11:48'

# 独立使用django的model
import os
import sys

# 当前文件所在目录
pwd = os.path.dirname(os.path.realpath(__file__))
# 获取工程根目录下的backend目录
pwd = os.path.join(os.path.dirname(os.path.dirname(pwd)), 'backend')
sys.path.append(pwd)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dyezweb.settings')

import django
django.setup()

from students.models import Student

from tools.db.data.students_data import raw_data

for student_detail in raw_data:
    student = Student()
    student.name = student_detail["name"]
    student.gender = student_detail["gender"]
