# _*_ coding: utf-8 _*_
__author__ = 'Yang Haibo'
__date__ = '2020/5/7 10:27'


import xadmin
from .models import Area


class AreaAdmin(object):
    # model_icon = 'fa fa-home'
    list_display = ['id', 'name', 'parent']
    list_filter = ['parent']
    search_fields = ['name']

xadmin.site.register(Area, AreaAdmin)
