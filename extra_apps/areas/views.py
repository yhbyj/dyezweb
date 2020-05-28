# ViewSets define the view behavior.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from .filters import AreaFilter
from .models import Area
from .pagers import AreaPagination
from .serializers import AreaSerializer


class AreaViewSet(viewsets.ModelViewSet):
    """
    list:
        行政区划信息列表
    """
    queryset = Area.objects.all()
    # 准备省级行政区划数据，便于从最高层开始数据序列化和展示
    # queryset = Area.objects.filter(area_type=1)
    serializer_class = AreaSerializer
    pagination_class = AreaPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # filter_fields = ['parent']
    search_fields = ['name', 'parent']
    filterset_class = AreaFilter
