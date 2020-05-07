# _*_ coding: utf-8 _*_
__author__ = 'Yang Haibo'
__date__ = '2020/5/7 12:21'

import xadmin
from .models import ServiceCategory, SPU, SPUSpecification, SpecificationOption
from .models import SKU, SKUImage, SKUSpecification


class ServiceCategoryAdmin(object):
    """
    服务类型管理
    """
    list_display = ["name", "parent", "create_time"]
    list_filter = ["parent", "name"]
    search_fields = ['name']


class SPUAdmin(object):
    """
    服务SPU管理
    """
    list_display = ["name"]
    search_fields = ['name']
    list_filter = ["name"]
    style_fields = {"detail": "ueditor"}


class SPUSpecificationAdmin(object):
    """
    服务SPU规格管理
    """
    list_display = ["name"]
    search_fields = ['name']
    list_filter = ["name"]

    class SpecificationOptionInline(object):
        model = SpecificationOption
        exclude = ["create_time"]
        extra = 1
        style = 'tab'

    inlines = [SpecificationOptionInline]


class SKUAdmin(object):
    """
    服务SKU管理
    """
    list_display = ["name", "fee", "quotas", "comments", "is_launched"]
    search_fields = ['name']
    list_filter = ["name"]

    class SKUImagesInline(object):
        model = SKUImage
        exclude = ["create_time"]
        extra = 1
        style = 'tab'

    inlines = [SKUImagesInline]

    # class SKUSpecificationInline(object):
    #     model = SKUSpecification
    #     exclude = ["create_time"]
    #     extra = 1
    #     style = 'tab'

    # inlines = [SKUImagesInline, SKUSpecificationInline]


class SKUSpecificationAdmin(object):
    """
    SKU具体规格管理
    """
    list_display = ["sku", "spec", "option"]
    search_fields = ["sku", "spec", "option"]
    list_filter = ["sku", "spec", "option"]


xadmin.site.register(ServiceCategory, ServiceCategoryAdmin)
xadmin.site.register(SPU, SPUAdmin)
xadmin.site.register(SPUSpecification, SPUSpecificationAdmin)
xadmin.site.register(SKU, SKUAdmin)
xadmin.site.register(SKUSpecification, SKUSpecificationAdmin)




