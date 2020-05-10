from django.contrib import admin

# Register your models here.


from .models import ServiceCategory, SPU, SPUSpecification, SpecificationOption
from .models import SKU, SKUImage, SKUSpecification


class ServiceCategoryAdmin(admin.ModelAdmin):
    """
    服务类型管理
    """
    list_display = ["name", "parent", "create_time"]
    list_filter = ["parent", "name"]
    search_fields = ['name']


class SPUAdmin(admin.ModelAdmin):
    """
    服务SPU管理
    """
    list_display = ["name"]
    search_fields = ['name']
    list_filter = ["name"]


class SPUSpecificationAdmin(admin.ModelAdmin):
    """
    服务SPU规格管理
    """
    list_display = ["name"]
    search_fields = ['name']
    list_filter = ["name"]

    class SpecificationOptionInline(admin.StackedInline):
        model = SpecificationOption

    inlines = [SpecificationOptionInline]


class SKUAdmin(admin.ModelAdmin):
    """
    服务SKU管理
    """
    list_display = ["name", "fee", "quotas", "comments", "is_launched"]
    search_fields = ['name']
    list_filter = ["name"]

    class SKUImagesInline(admin.TabularInline):
        model = SKUImage

    inlines = [SKUImagesInline]


class SKUSpecificationAdmin(admin.ModelAdmin):
    """
    SKU具体规格管理
    """
    list_display = ["sku", "spec", "option"]
    search_fields = ["sku", "spec", "option"]
    list_filter = ["sku", "spec", "option"]


admin.site.register(ServiceCategory, ServiceCategoryAdmin)
admin.site.register(SPU, SPUAdmin)
admin.site.register(SPUSpecification, SPUSpecificationAdmin)
admin.site.register(SKU, SKUAdmin)
admin.site.register(SKUSpecification, SKUSpecificationAdmin)