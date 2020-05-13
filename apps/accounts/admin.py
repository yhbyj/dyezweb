from django.contrib import admin
from .models import Account


# Register your models here.
# django.core.exceptions.ImproperlyConfigured: Put 'django.contrib.contenttypes'
# in your INSTALLED_APPS setting in order to use the admin application.
class AccountAdmin(admin.ModelAdmin):
    """
    用户账户类型管理
    """
    # change list page options
    date_hierarchy = 'date_joined'
    empty_value_display = '-空-'
    list_display = ['username', 'email', 'email_active', 'mobile', 'last_login', 'first_name', 'last_name',
                    'is_superuser', 'is_active', 'is_staff', 'date_joined']
    list_filter = ['is_superuser', 'is_active', 'is_staff', 'date_joined', 'email_active', 'last_name']
    search_fields = ['username', 'email', 'mobile']
    list_editable = ['mobile', 'is_superuser', 'is_active', 'is_staff']

    # control the layout of admin “add” and “change” pages
    readonly_fields = ['email_active', 'last_login', 'date_joined']
    fieldsets = (
        (None, {
            'fields': (('username', 'password'), ('email', 'email_active', 'mobile'),
                       ('is_superuser', 'is_active', 'is_staff'))
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': (('first_name', 'last_name'), ('last_login', 'date_joined')),
        }),
    )



admin.site.site_header = '中职信息管理系统-后台'
admin.site.site_title = '中职信息管理系统-后台'

admin.site.register(Account, AccountAdmin)

