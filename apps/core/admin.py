from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from core import models


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


# 设置icon,学生管理这个菜单默认的icon是个圆圈不好看,接下来，就是设置菜单项的icon
# 图标来源:  http://fontawesome.dashgame.com/ 如果想要换其它的图标，可以去这里找。
class StudentAdmin(admin.ModelAdmin):
    model_icon = 'fa fa-home'


class TopMajorCategoryListFilter(admin.SimpleListFilter):
    """
    一级专业类别列表筛选类
    """
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = '一级专业类别'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'top_category_id_exact'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        # 获得一级专业类别的数据
        rs = set([c for c in MajorCategory.objects.filter(category_type=1)])
        v = set()
        for obj in rs:
            if obj is not None:
                v.add((obj.id, obj.name))
        return v

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value
        # to decide how to filter the queryset.
        if 'top_category_id_exact' in request.GET:
            top_category_id = request.GET['top_category_id_exact']
            return queryset.filter(category__parent_category_id=top_category_id)
        else:
            return queryset.all()


class MajorCategoryAdmin(admin.ModelAdmin):
    """
    专业类别模型管理
    """
    # change list page options
    list_display = ['name', 'category_type', 'parent_category', 'desc',
                    'create_time', 'update_time', 'is_delete']
    list_filter = ['category_type', 'create_time', 'update_time', 'is_delete']
    search_fields = ['name', 'desc']

    # control the layout of admin “add” and “change” pages
    fields = ['name', 'category_type', 'parent_category', 'desc']
    radio_fields = {"category_type": admin.HORIZONTAL}


class MajorAdmin(admin.ModelAdmin):
    """
    专业类模型管理
    """
    # def bottom_category(self, obj):
    #     """
    #     获取末级专业类别（即二级类别）数据
    #     :param obj:
    #     :return:
    #     """
    #     return MajorCategory.objects.filter(category_type=2)

    # bottom_category = MajorCategory.objects.filter(category_type=2)

    # change list page options
    list_display = ['short_code', 'name', 'category', 'status', 'create_time', 'update_time', 'is_delete', 'code']
    list_display_links = ['name']
    list_filter = [TopMajorCategoryListFilter, 'status', 'create_time', 'update_time', 'is_delete']
    list_editable = ['status']

    # control the layout of admin “add” and “change” pages
    fields = ['short_code', 'name', 'category', 'status', 'code']


class AdmissionMajorInline(admin.TabularInline):
    """
    入学申请和专业内联类
        Working with many-to-many intermediary models
    """
    model = models.AdmissionMajor
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
                    'user', 'filler', 'adviser', 'address', 'zip_code', 'mobile', 'telephone_number',
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
                       ('user', 'filler', 'create_time', 'update_time', 'is_delete'))
        }),
        ('以下内容由学校填写', {
            'classes': ('wide', 'extrapretty'),
            'fields': (('confirmed', 'confirmed_by', 'confirmed_on'), 'confirmed_with', 'memo'),
        }),
    )

    # form = AdmissionAdminForm


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


class ThreeCompetitionRuleCategoryAdmin(admin.ModelAdmin):
    """
    三项竞赛评分细则类别模型管理
    """
    # change list page options
    list_display = ['name', 'category_type', 'parent_category', 'desc',
                    'create_time', 'update_time', 'is_delete']
    list_filter = ['category_type', 'create_time', 'update_time', 'is_delete']
    search_fields = ['name', 'desc']

    # control the layout of admin “add” and “change” pages
    fields = ['category_type', 'parent_category',  'name', 'desc']
    radio_fields = {"category_type": admin.HORIZONTAL}


# class TopThreeCompetitionRuleCategoryListFilter(admin.SimpleListFilter):
class TopTcrcListFilter(admin.SimpleListFilter):
    """
    三项竞赛评分细则类别列表筛选类
    """
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = '一级类别'

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'top_category_id_exact'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        # 获得一级三项竞赛评分细则类别的数据
        rs = set([c for c in Tcrc.objects.filter(category_type=1)])
        v = set()
        for obj in rs:
            if obj is not None:
                v.add((obj.id, obj.name))
        return v

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value
        # to decide how to filter the queryset.
        if 'top_category_id_exact' in request.GET:
            top_category_id = request.GET['top_category_id_exact']
            return queryset.filter(category__parent_category_id=top_category_id)
        else:
            return queryset.all()


class ThreeCompetitionRuleOptionInline(admin.TabularInline):
    """
    三项竞赛评分细则和选项内联类
    """
    model = models.ThreeCompetitionRuleOption
    extra = 1


class ThreeCompetitionRuleAdmin(admin.ModelAdmin):
    """
    三项竞赛评分细则类模型管理
    """
    inlines = [ThreeCompetitionRuleOptionInline]

    # change list page options
    list_display = ['name', 'category', 'create_time', 'update_time', 'is_delete', 'code']
    list_display_links = ['name']
    list_filter = [TopTcrcListFilter, 'create_time', 'update_time', 'is_delete']

    # control the layout of admin “add” and “change” pages
    fields = ['category', 'name', 'code', 'desc', 'min', 'max']


class DormitoryCompetitionAdmin(admin.ModelAdmin):
    """
    寝室竞赛类模型管理
    """
    # change list page options
    date_hierarchy = 'create_time'
    list_display = ['dormitory', 'option', 'score', 'is_minus']
    list_display_links = ['option']
    list_filter = ['is_minus']
    search_fields = ['dormitory', 'option']

    # control the layout of admin “add” and “change” pages
    fields = ['dormitory', 'option', 'score', 'is_minus']


admin.site.site_header = '中职信息管理系统-后台'
admin.site.site_title = '中职信息管理系统-后台'

admin.site.register(models.User, UserAdmin)
admin.site.register(models.Tag)
admin.site.register(models.Ingredient)
admin.site.register(models.Recipe)
admin.site.register(models.SmsCode, SmsCodeAdmin)
admin.site.register(models.Student, StudentAdmin)
admin.site.register(models.MajorCategory, MajorCategoryAdmin)
admin.site.register(models.Major, MajorAdmin)
admin.site.register(models.Admission, AdmissionAdmin)
admin.site.register(models.Dormitory, DormitoryAdmin)
admin.site.register(models.ThreeCompetitionRuleCategory, ThreeCompetitionRuleCategoryAdmin)
admin.site.register(models.ThreeCompetitionRule, ThreeCompetitionRuleAdmin)
admin.site.register(models.DormitoryCompetition, DormitoryCompetitionAdmin)
