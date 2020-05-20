#应用部署（_deployment）手册
有多种部署方式，每种部署方式又分为本地(local)和线上(online)。  
本地环境一般是 windows系统  
线上环境一般是 linux系统  
requirements_extra.txt  pip 安装时的附加包信息。
##传统部署方式(legacy)
###local 
###online
##docker部署方式
###local
移动并覆盖 settings.py 文件。 
复制 local.yml 文件到项目根目录，并运行：   
```commandline
docker-compose -f local.yml build
docker-compose -f local.yml up
```
###online
移动并覆盖 settings.py 文件。 
复制 online.yml 文件到项目根目录，并运行：  
```commandline
docker stack deploy -c online.yml dyezweb
```
