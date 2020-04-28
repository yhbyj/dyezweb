from django.db import models

# Create your models here.
class Student(models.Model):
    gender_choices = (
        (0, '男'),
        (1, '女'),
    )
    name = models.CharField(max_length=50, verbose_name='姓名')
    # gender = models.CharField(max_length=10, default='男', choices=(("男", "男"), ("女", "女")), verbose_name='性别')
    gender = models.SmallIntegerField(default=0, choices=gender_choices, verbose_name='性别')
    age = models.IntegerField(default=0, verbose_name='年龄')
    createTime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    class Meta:
        # zz: 中职
        db_table ='zz_student'
        verbose_name ="学生"
        verbose_name_plural = verbose_name
    ordering = ['-createTime']
    def __str__(self):
        return self.name