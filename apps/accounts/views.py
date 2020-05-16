from random import choice

from rest_framework import viewsets, status
from rest_framework.mixins import CreateModelMixin
from rest_framework.response import Response

from dyezweb.settings.common import APIKEY
from utils.yunpian import YunPian
from .models import Account, SmsCode
from .serializers import SmsCodeSerializer, AccountRegSerializer


# Create your views here.
# ViewSets define the view behavior.
class AccountViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """

    """
    queryset = Account.objects.all()
    serializer_class = AccountRegSerializer


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

