from django.contrib import admin
from django import forms


# Register your models here.

from .models import Admission


class AdmissionAdminForm(forms.ModelForm):
    """
    自定义数据验证（后台），其实在数据模型里就可以直接验证。
    """
    pass


class AdmissionAdmin(admin.ModelAdmin):
    """
    入学申请（报名）类型管理
    """
    list_display = ['name', 'sex', 'hukou', 'nationality', 'native_place', 'id_card_no',
                    'political_status', 'health_status', 'origin', 'parent_name', 'graduate_school', 'position']
    list_filter = ['sex', 'hukou', 'nationality', 'native_place', 'political_status',
                   'health_status', 'origin', 'graduate_school', 'position']
    search_fields = ['name', 'id_card_no', 'parent_name']

    form = AdmissionAdminForm


admin.site.register(Admission, AdmissionAdmin)
