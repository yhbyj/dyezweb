from django.db import models
from utils.db.base_model import BaseModel


# Create your models here.
class Major(BaseModel):
    """
    专业模型类
    """
    status_choices = (
        (0, '下线'),
        (1, '上线'),
    )
    title = models.CharField(max_length=50, verbose_name='名称')
    status = models.SmallIntegerField(default=1, choices=status_choices, verbose_name='专业状态')

    class Meta:
        db_table = 'tb_major'
        verbose_name = "专业"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
