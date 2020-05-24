from django.contrib import admin

from .models import ThreeCompetitionRule, ThreeCompetitionRuleCategory as Tcrc, DormitoryCompetition, \
    ThreeCompetitionRuleOption


# Register your models here.
class TcrcAdmin(admin.ModelAdmin):
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
    model = ThreeCompetitionRuleOption
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


admin.site.register(Tcrc, TcrcAdmin)
admin.site.register(ThreeCompetitionRule, ThreeCompetitionRuleAdmin)
admin.site.register(DormitoryCompetition, DormitoryCompetitionAdmin)