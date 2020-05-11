# _*_ coding: utf-8 _*_
__author__ = 'Yang Haibo'
__date__ = '2020/5/10 21:38'

from rest_framework.pagination import PageNumberPagination


class AccountPagination(PageNumberPagination):
    """
    用户账户分页类
    """
    page_size = 5
    page_size_query_param = 'page_size'
    page_query_param = 'p'
    max_page_size = 100