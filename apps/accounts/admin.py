from django.contrib import admin
from .models import Account
# Register your models here.


# django.core.exceptions.ImproperlyConfigured: Put 'django.contrib.contenttypes'
# in your INSTALLED_APPS setting in order to use the admin application.

admin.site.site_header = '中职信息管理系统-后台'
admin.site.site_title = '中职信息管理系统-后台'

admin.site.register(Account)
