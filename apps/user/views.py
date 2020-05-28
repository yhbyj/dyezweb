# from django.shortcuts import render
from random import choice

from rest_framework import generics, viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.settings import api_settings

from core.models import User, SmsCode
from .serializers import UserSerializer, AuthTokenSerializer, SmsCodeSerializer


class CreateUserView(generics.CreateAPIView):
    """在系统里创建一个新用户"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """为用户创建一个令牌"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """管理通过验证的用户"""
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user


class SmsCodeViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码
    """
    queryset = SmsCode.objects.all()
    serializer_class = SmsCodeSerializer

    def generate_code(self):
        """
        生成四位数字的验证码
        :return:
        """
        seeds = '1234567890'
        numbers = []
        for i in range(4):
            numbers.append(choice(seeds))
        return ''.join(numbers)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data['mobile']
        code = self.generate_code()

        # 通过第三方平台发短信送验证码
        # yun_pian = YunPian(APIKEY)
        # code = self.generate_code()
        # sms_status = yun_pian.send_sms(code=code, mobile=mobile)

        # 测试用,假设发送成功!
        sms_status = {"code": 0}
        if sms_status["code"] != 0:
            return Response({
                "mobile": sms_status["msg"]
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = SmsCode(code=code, mobile=mobile)
            code_record.save()
            return Response({
                "mobile": mobile
            }, status=status.HTTP_201_CREATED)

        # self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        # return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

