# _*_ coding: utf-8 _*_
__author__ = 'Yang Haibo'
__date__ = '2020/5/7 20:30'

import xadmin
from .models import Admission


class AdmissionAdmin(object):
    """
    入学申请（报名）类型管理
    """
    list_display = ['name', 'sex', 'hukou', 'nationality', 'native_place', 'id_card_no',
                    'political_status', 'health_status', 'origin', 'parent_name', 'graduate_school', 'position']
    list_filter = ['sex', 'hukou', 'nationality', 'native_place', 'political_status',
                   'health_status', 'origin', 'graduate_school', 'position']
    search_fields = ['name', 'id_card_no', 'parent_name']


xadmin.site.register(Admission, AdmissionAdmin)

