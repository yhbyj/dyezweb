from django.contrib import admin
from django import forms


# Register your models here.
from majors.models import Major
from .models import Admission, AdmissionMajor


class AdmissionAdminForm(forms.ModelForm):
    """
    自定义数据验证（后台），其实在数据模型里就可以直接验证。
    """
    pass


class AdmissionMajorInline(admin.TabularInline):
    """
    入学申请和专业内联类
        Working with many-to-many intermediary models
    """
    model = AdmissionMajor
    extra = 1

class AdmissionAdmin(admin.ModelAdmin):
    """
    入学申请（报名）类型管理
    """
    def get_majors(self, obj):
        """
        根据入学申请表ID获得专业ID
        :param obj:
        :return:
        """
        return [a.major for a in AdmissionMajor.objects.fiter(admission=obj.id)]

    # 默认位置在最下方,如何调整位置?
    inlines = [AdmissionMajorInline]

    # change list page options
    date_hierarchy = 'create_time'
    empty_value_display = '-空-'
    # The value of 'list_display[12]' must not be a ManyToManyField ('majors').
    list_display = ['name', 'sex', 'hukou', 'nationality', 'native_place', 'id_card_no', 'political_status',
                    'health_status', 'origin', 'parent_name', 'graduate_school', 'position',
                    'account', 'filler', 'adviser', 'address', 'zip_code', 'mobile', 'telephone_number',
                    'create_time', 'update_time', 'is_delete',
                    'confirmed', 'confirmed_with', 'confirmed_by', 'confirmed_on', 'memo']
    list_filter = ['sex', 'hukou', 'political_status', 'health_status',
                   'origin', 'adviser', 'zip_code', 'majors',
                   'create_time', 'update_time', 'is_delete', 'confirmed']
    search_fields = ['name', 'nationality', 'graduate_school', 'id_card_no', 'mobile', 'majors']
    list_editable = ['id_card_no', 'is_delete', 'confirmed']

    # control the layout of admin “add” and “change” pages
    readonly_fields = ['create_time', 'update_time']
    radio_fields =  {"sex": admin.HORIZONTAL, "hukou": admin.HORIZONTAL,
                     "political_status": admin.HORIZONTAL, "health_status": admin.HORIZONTAL,
                     "origin": admin.HORIZONTAL}
    fieldsets = (
        (None, {
            'fields': (('name', 'sex', 'hukou', 'nationality', 'native_place'), 'id_card_no',
                       ('political_status', 'health_status', 'origin'),
                       ('parent_name', 'address', 'zip_code', 'mobile', 'telephone_number'),
                       ('graduate_school', 'position'),
                       ('account', 'filler', 'create_time', 'update_time', 'is_delete'))
        }),
        ('以下内容由学校填写', {
            'classes': ('wide', 'extrapretty'),
            'fields': (('confirmed', 'confirmed_by', 'confirmed_on'), 'confirmed_with', 'memo'),
        }),
    )

    # form = AdmissionAdminForm


admin.site.register(Admission, AdmissionAdmin)
