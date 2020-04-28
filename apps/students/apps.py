from django.apps import AppConfig


class StudentsConfig(AppConfig):
    name = 'students'
    # 后台管理 students app 时标题中文显示
    verbose_name = '学生管理'
