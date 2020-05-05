# _*_ coding: utf-8 _*_
__author__ = 'Yang Haibo'
__date__ = '2020/4/28 20:43'

import xadmin
from students import models

# 设置icon,学生管理这个菜单默认的icon是个圆圈不好看,接下来，就是设置菜单项的icon
# 图标来源:  http://fontawesome.dashgame.com/ 如果想要换其它的图标，可以去这里找。
class StudentAdmin(object):
    model_icon = 'fa fa-home'

xadmin.site.register(models.Student, StudentAdmin)