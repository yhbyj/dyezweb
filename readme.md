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
不开放注册，直接线下获取用户手机号或电子邮箱（如QQ邮箱），在后台注册，生成登录账号和密码。
用户根据获取的账号（手机号或电子邮箱）和密码登录，完善报名信息。
```
##第四天  
### 针对django2.2报错：UnicodeDecodeError: ‘gbk’ codec can’t decode byte 0xa6 in position 9737: ill…  

```text
https://blog.csdn.net/weixin_43279476/article/details/91951235
1、报错：
File “D:\Python\Python37-32\lib\site-packages\django\views\debug.py”, line 332, in get_traceback_html
t = DEBUG_ENGINE.from_string(fh.read())
UnicodeDecodeError: ‘gbk’ codec can’t decode byte 0xa6 in position 9737: illegal multibyte sequence
2、解决：
打开django/views下的debug.py文件，转到line331行：
with Path(CURRENT_DIR, ‘templates’, ‘technical_500.html’).open() as fh
将其改成：
with Path(CURRENT_DIR, ‘templates’, ‘technical_500.html’).open(encoding=“utf-8”) as fh
就成功了。
```
###数据验证  
```text
1、数据模型类中重写 clean 方法；
2、注册数据模型到后台管理时，创建继承forms.ModelForm的类；
```
###数据库和模型类：账户信息、监护人等   
```text
1、users -> accounts
2、guardians
```
##第五天   
### viewsets.ModelViewSet   
```text
序列化： serializer_class  
分页： pagination_class  
过滤： filterset_class
搜索： search_fields
```
###后台管理   
```text
InlineModelAdmin: Working with many-to-many intermediary models
```