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
入学申请和专业之间的多对多关系：一人可以申请多个专业，一个专业可以被多个人申请
```
##第六天 
### 模型类  
```text
专业类：Major
专业类别类：MajorCategory
```  
### 后台管理  
```text
自定义过滤类：class TopMajorCategoryListFilter(admin.SimpleListFilter)
```
##第七天 
### 准备测试数据  
```text
excel_to_sql： {"sqlite": datetime('now','localtime'), "sql":now()}
```  
### 数据验证    
```text
django.core.validators  on model level
```  
##第八天
###上线测试
```text
分离 settings 文件： local and online
docker-compose -f online.yml build
docker-compose -f online.yml up
```
##第九天 
### 用户注册功能和序列化  
```text
增加“短信验证码”数据模型
SmsCodeSerializer
AccountRegSerializer  
```  
##第十天 
### 目录结构和配置文件随部署方式的调整 
```text
配置文件保留原样！各种部署方式自带配置文件！ 
```  
##第十一天 
### 自动化部署（legacy online）
```text
_deployment/legacy/online/fabfile.py
``` 
### docker 方式部署（local online）
```text
_deployment/docker/local/local.yml
_deployment/docker/local/django/Dockerfile
``` 
复制 local.yml 文件到项目根目录，并运行：   
```commandline
docker-compose -f local.yml build
docker-compose -f local.yml up
```
##第十二天 
### 第三方认证（social app django）
```text
复制 social_core 到 extra_apps下，并修改下面的文件，以支持 drf token 认证。
extra_apps\social_core\actions.py
from rest_framework.authtoken.models import Token
……
def do_complete(backend, login, user=None, redirect_name='next',
                *args, **kwargs):
……
    return backend.strategy.redirect(url)
    '''
    response = backend.strategy.redirect(url)
    token = Token.objects.get(user_id=user.id)
    response.set_cookies('name', user.username, max_age=24*3600)
    response.set_cookies('token', token.key, max_age=24*3600)
    return response
    '''
``` 
### 错误日志收集和管理（sentry）
```text
在docker desktop中搭建失败：
git clone https://github.com/getsentry/onpremise.git
cd onpremise
./install.sh
……
FAIL: Cannot read credentials back from relay/credentials.json.
      Please ensure this file is readable and contains valid credentials.

docker destop 回复出厂设置，git 发行版，成功！
git clone -b releases/9.1.x https://github.com/getsentry/onpremise.git
cd onpremise
./install.sh
……
docker-compose up -d
访问9000端口！
``` 
##第十三天 
### 三项竞赛（卫生、纪律和文礼）
```text
完成“寝室竞赛”：DormitoryCompetition
``` 
##第十四天 
### TDD & docker & Travis CI  
所有的数据模型类都在 core app 中  
```commandline
docker-compose run --rm dyezweb sh -c "python manage.py startapp core"
docker-compose run --rm dyezweb sh -c "python manage.py makemigrations core"
docker-compose build
docker-compose up
``` 
```text
Added endpoint for creating users
```
##第十五天 
### 统一docker部署  
```text
不分本地和远程
增加远程自动化迭代部署
第一次远程部署
git clone https://gitee.com/zjdyez/dyezweb.git
docker-compose build
docker-compose up
第N次远程部署
docker-compose down
git pull
docker-compose build
docker-compose up
```
### 增加对 image 字段的支持  
##第十六天 
### 对先前已经编好的代码进行测试
```commandline
 docker-compose run dyezweb sh -c "python manage.py test core && flake8 apps/core"
 docker-compose run dyezweb sh -c "python manage.py test user && flake8 apps/user"
 docker-compose run dyezweb sh -c "python manage.py test recipe && flake8 apps/recipe"
 docker-compose run dyezweb sh -c "python manage.py test student && flake8 apps/student"
```  
