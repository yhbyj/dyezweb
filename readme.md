#中职学校信息管理系统
##第一天  
###参考  
[Django2.2配置xadmin](https://blog.csdn.net/weixin_44944640/article/details/89402815)   
[django2使用xadmin打造适合国人的后台管理系统（1）](https://www.jianshu.com/p/9b3bfe934511)
[美多商城](https://gitee.com/zjdyez/meduo.site)    
###开发环境  
```text
Python  3.6.8
Django  2.2
xadmin  https://github.com/sshwsfc/xadmin/tree/django2
```
```commandline
pip install --upgrade framework six django-import-export django-formtools future httplib2 django-crispy-forms -i https://mirrors.aliyun.com/pypi/simple
```
##第二天   
###django rest framework  
```commandline
pip install  djangorestframework markdown django-filter
```  
###前后端分离  
```text
backend 后端
frontend_pc PC前端
rest_framework.authtoken    api-token-auth/
```
##第三天  
###数据库和模型类
```text
商品和服务的关系：该网站不提供具体的商品，但提供服务，例如入学申请服务。
该网站不是商业网站，但服务是有限额的，也不是免费的，还需要在线申请和双向确认。
具体的数据表有：服务类型、服务（SPU）、SPU规格、规格选项、服务（SKU）、SKU规格
例如：由东阳市职教中心校办发起的“2020年东阳市职教中心招生”服务，
属于“招生”类服务，服务规格包括校区、专业等。
```
###网上入学报名（admissions app）  
```text
不开放注册，直接线下获取用户身份证、手机号或电子邮箱，在后台注册，生成登录账号和密码。
用户根据获取的账号（身份证、手机号或电子邮箱）和密码登录，完善报名信息。
```