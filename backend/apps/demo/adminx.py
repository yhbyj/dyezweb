# _*_ coding: utf-8 _*_
__author__ = 'Yang Haibo'
__date__ = '2020/4/28 20:22'

import xadmin

# Register your models here.

from xadmin import views

# django.core.exceptions.ImproperlyConfigured: Put 'django.contrib.contenttypes'
# in your INSTALLED_APPS setting in order to use the admin application.
class GlobalSetting(object):
    # 设置后台顶部标题
    site_title ='中职信息管理系统-后台'
    # 设置后台底部标题
    site_footer ='2020'
    # 设置菜单可折叠
    menu_style = "accordion"

class BaseSetting(object):
    # 启用主题管理器
    enable_themes =True
    # 使用主题
    use_bootswatch =True

xadmin.site.register(views.CommAdminView, GlobalSetting)
# 注册主题设置
xadmin.site.register(views.BaseAdminView, BaseSetting)