from django.db import models
from utils.db.base_model import BaseModel

# Create your models here.
class Student(BaseModel):
    """
    学生模型类
    """
    gender_choices = (
        (0, '男'),
        (1, '女'),
    )
    status_choices = (
        (0, '下线'),
        (1, '上线'),
    )
    name = models.CharField(max_length=50, verbose_name='姓名')
    # gender = models.CharField(max_length=10, default='男', choices=(("男", "男"), ("女", "女")), verbose_name='性别')
    gender = models.SmallIntegerField(default=0, choices=gender_choices, verbose_name='性别')
    # age = models.IntegerField(default=0, verbose_name='年龄')
    status = models.SmallIntegerField(default=1, choices=status_choices, verbose_name='学生状态')
    clazz = models.ForeignKey('clazzs.Clazz', on_delete=models.CASCADE, verbose_name='班级')
    major = models.ForeignKey('majors.Major', on_delete=models.CASCADE, verbose_name='专业')

    class Meta:
        # zz: 中职
        db_table = 'tb_student'
        verbose_name = "学生"
        verbose_name_plural = verbose_name

    # ordering = ['-create_time']
    def __str__(self):
        return self.name
