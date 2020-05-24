from django.contrib import admin

# Register your models here.
from .models import Dormitory


class DormitoryAdmin(admin.ModelAdmin):
    """
    学生宿舍类模型管理
    """
    # change list page options
    list_display = ['building', 'short_code', 'name', 'beds', 'with_bathroom']
    list_display_links = ['short_code']
    list_filter = ['building', 'beds', 'with_bathroom']

    # control the layout of admin “add” and “change” pages
    fields = ['building', 'short_code', 'name', 'beds', 'with_bathroom']


admin.site.register(Dormitory, DormitoryAdmin)