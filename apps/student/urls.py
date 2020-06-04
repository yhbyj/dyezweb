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
router.register('dormitories', views.DormitoryViewSet)
router.register('three-competition-rule-categories',
                views.ThreeCompetitionRuleCategoryViewSet)
router.register('three-competition-rules',
                views.ThreeCompetitionRuleViewSet)
router.register('three-competition-rule-options',
                views.ThreeCompetitionRuleOptionViewSet)
router.register('dormitory-competitions',
                views.DormitoryCompetitionViewSet)


app_name = 'student'

urlpatterns = [
    path('', include(router.urls))
]
