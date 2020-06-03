# _*_ coding: utf-8 _*_
__author__ = 'Yang Haibo'
__date__ = '2020/6/1 16:00'

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from student import views

router = DefaultRouter()
router.register('admissions', views.AdmissionViewSet)
router.register('major-categories', views.MajorCategoryViewSet)
router.register('majors', views.MajorViewSet)


app_name = 'student'

urlpatterns = [
    path('', include(router.urls))
]
