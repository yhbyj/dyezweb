# _*_ coding: utf-8 _*_
__author__ = 'Yang Haibo'
__date__ = '2020/5/8 14:42'

import xadmin
from xadmin import views
from areas.models import Area
from .models import User

# Register your models here.


class GlobalSetting(object):
    # 设置后台顶部标题
    site_title = '中职信息管理系统-后台'
    # 设置后台底部标题
    site_footer = '东阳二职'
    # 设置菜单可折叠
    menu_style = "accordion"


class BaseSetting(object):
    # 启用主题管理器
    enable_themes = True
    # 使用主题
    use_bootswatch = True


class AreaAdmin(object):
    # model_icon = 'fa fa-home'
    list_display = ['id', 'name', 'parent']
    list_filter = ['parent']
    search_fields = ['name']


xadmin.site.register(views.CommAdminView, GlobalSetting)
# 注册主题设置
xadmin.site.register(views.BaseAdminView, BaseSetting)

xadmin.site.unregister(User)
xadmin.site.register(User)
xadmin.site.register(Area, AreaAdmin)

