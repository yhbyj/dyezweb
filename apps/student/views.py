from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core import models
from student import serializers


class MajorCategoryViewSet(viewsets.ModelViewSet):
    """管理数据库中的专业类别信息"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = models.MajorCategory.objects.all()
    serializer_class = serializers.MajorCategorySerializer

    def get_queryset(self):
        """返回所有一级专业类别对象"""
        return self.queryset.filter(
            category_type=1
        ).order_by('-id')


class MajorViewSet(viewsets.ModelViewSet):
    """管理数据库中的专业信息"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = models.Major.objects.all()
    serializer_class = serializers.MajorSerializer

    def get_queryset(self):
        """返回所有一级专业类别对象"""
        return self.queryset.all().order_by('-id')


class AdmissionViewSet(viewsets.ModelViewSet):
    """管理数据库中的入学报名信息"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = models.Admission.objects.all()
    serializer_class = serializers.AdmissionSerializer

    def _params_to_ints(self, qs):
        """把字符串形式的ID列表，转换成整型形式的ID列表，并返回"""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """仅返回当前登录用户输入的入学申请"""
        majors = self.request.query_params.get('majors')
        queryset = self.queryset
        if majors:
            major_ids = self._params_to_ints(majors)
            queryset = queryset.filter(majors__id__in=major_ids)

        return queryset.filter(
            user=self.request.user
        ).order_by('-id')

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.AdmissionDetailSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        """创建入学申请"""
        serializer.save(user=self.request.user)
