# from django.shortcuts import render
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from core.models import User
from .serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """在系统里创建一个新用户"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """为用户创建一个令牌"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


