from django.contrib import admin

from majors.models import Major
from .models import Major, MajorCategory


# Register your models here.
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
    list_display = ['name', 'category_type', 'parent_category', 'is_tab', 'desc',
                    'create_time', 'update_time', 'is_delete']
    list_filter = ['category_type', 'is_tab',
                   'create_time', 'update_time', 'is_delete']
    search_fields = ['name', 'desc']
    list_editable = ['is_tab']

    # control the layout of admin “add” and “change” pages
    fields = ['name', 'category_type', 'parent_category', 'is_tab', 'desc']
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


admin.site.register(MajorCategory, MajorCategoryAdmin)
admin.site.register(Major, MajorAdmin)