# _*_ coding: utf-8 _*_
__author__ = 'Yang Haibo'
__date__ = '2020/5/11 7:47'


from rest_framework.pagination import PageNumberPagination


class AreaPagination(PageNumberPagination):
    """
    行政区划分页类
    """
    page_size = 100
    page_size_query_param = 'page_size'
    page_query_param = 'p'
    max_page_size = 1000