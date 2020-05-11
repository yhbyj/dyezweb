from django.shortcuts import render
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from .models import Account
from .serializers import AccountSerializer
from .pagers import AccountPagination
from .filters import AccountFilter

# Create your views here.


# ViewSets define the view behavior.
class AccountViewSet(viewsets.ModelViewSet):
    """
    list:
        用户账户列表
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    pagination_class = AccountPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filter_fields = ['username', 'date_joined']
    search_fields = ['username', 'email']
    # filterset_class = AccountFilter