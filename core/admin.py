from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from .models import User, SmsCode


class UserAdmin(BaseUserAdmin):
    """用户类型管理"""
    # 用户列表页
    ordering = ['id']
    list_display = ['mobile', 'name']
    # 用户编辑页
    fieldsets = (
        (None, {'fields': ('mobile', 'password')}),
        (_('Personal Info'), {'fields': ('name', )}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important dates'), {'fields': ('last_login', )})
    )
    # 创建用户页
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),
            'fields': ('mobile', 'password1', 'password2')
        }),
    )


class SmsCodeAdmin(admin.ModelAdmin):
    """
    短信验证码类型管理
    """
    # change list page options
    date_hierarchy = 'add_time'
    list_display = ['mobile', 'code', 'add_time']
    search_fields = ['mobile']

    # control the layout of admin “add” and “change” pages
    fields = ['mobile', 'code', 'add_time']


admin.site.site_header = '中职信息管理系统-后台'
admin.site.site_title = '中职信息管理系统-后台'

admin.site.register(User, UserAdmin)
admin.site.register(SmsCode, SmsCodeAdmin)
