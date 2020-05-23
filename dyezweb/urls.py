"""dyezweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin
from rest_framework import routers

# xadmin 模块的父目录(extra_apps)已经 masked as Sources Root
import xadmin

# apps: rest_framework.authtoken
# By exposing an api endpoint
from rest_framework.authtoken import views

# 使用自定义的用户模型
# 自定义用户模块的父目录(apps)已经 masked as Sources Root
# Routers provide an easy way of automatically determining the URL conf.
from accounts.views import AccountViewSet, SmsCodeViewSet
from areas.views import AreaViewSet

router = routers.DefaultRouter()
router.register('accounts', AccountViewSet)
router.register('areas', AreaViewSet)
router.register('smscodes', SmsCodeViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    # 富文本相关url
    path('ueditor/', include('DjangoUeditor.urls')),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # 通过post方式提交json数据 {"username": "yhb","password": "123"}, 获得token
    # 测试软件： postman
    path('api-token-auth/', views.obtain_auth_token),

    # 第三方登录
    # 请求URL构造为：http://域名或者ip/login/使用模块名称小写/
    # 如：http://127.0.0.1:8000/login/weibo/
    # 回调URL构造为：http://域名或者ip/complete/使用模块名称小写/
    # 如：http://127.0.0.1:8000/complete/weibo/
    # 回调URL一般需要设置到开放平台的后台
    # 前台页面可以调用，请求url
    # <a href="{% url "social:begin" "weibo" %}">微博登录</a>
    path('', include('social_django.urls', namespace='social'))
]