#应用部署（_deployment）手册
部署方式：传统方式部署（legacy）、docker方式部署、k3s方式部署等。  
本地环境一般是 windows系统  
线上环境一般是 linux系统  
requirements_extra.txt  pip 安装时的附加包信息。
参考：[Django 学习小组](https://zhuanlan.zhihu.com/djstudyteam)
##传统部署方式(legacy)
###local 
###online 
####第一次，手工部署
查看系统环境  
```text
[root@localhost ~]# cat /etc/redhat-release   
CentOS Linux release 7.6.1810 (Core) 
[root@localhost ~]# whereis python3
python3: /usr/local/bin/python3.7m /usr/local/bin/python3.7 /usr/local/bin/python3.7m-config /usr/local/bin/python3 /usr/local/bin/python3.7-config /usr/local/lib/python3.7
[root@localhost ~]# python3
Python 3.7.7 (default, May 17 2020, 06:17:33) 
[GCC 4.8.5 20150623 (Red Hat 4.8.5-39)] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> exit()
[root@localhost ~]# whereis pip3
pip3: /usr/local/bin/pip3 /usr/local/bin/pip3.7
```
在虚拟环境中，准备源代码和软件包    
```commandline
su - yhb
mkvirtualenv -p /usr/local/bin/python3.7 dyezweb
mkdir projects
cd projects
git clone https://gitee.com/zjdyez/dyezweb.git
cd dyezweb/
cp _deployment/legacy/online/settings.py dyezweb/
cp _deployment/legacy/online/requirements_extra.txt ./
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple
pip install -r requirements_extra.txt -i https://mirrors.aliyun.com/pypi/simple
```
退出虚拟环境，启动监控   
```commandline
deactivate
pip3 install supervisor --user
mkdir -p ~/etc/supervisor/conf.d
mkdir -p ~/etc/supervisor/var/log
cd ~/etc
echo_supervisord_conf > supervisord.conf
vi supervisord.conf 
cd supervisor/conf.d/
vi dyezweb.ini
supervisord -c ~/etc/supervisord.conf
sudo setenforce 0
```
查看运行状态  
```text
[yhb@localhost ~]$ supervisorctl -c ~/etc/supervisord.conf status
dyezweb                          RUNNING   pid 11772, uptime 0:00:01
```
####第二次开始，自动部署
_deployment/legacy/online/fabfile.py   
##docker部署方式
###local online 
配置文件按线上标准配置，包含密钥，不提交到 github 或 gitee
复制 local.yml 文件到项目根目录，并运行：   
```commandline
docker-compose -f local.yml build
docker-compose -f local.yml up
```
###remote online
复制 online.yml 文件到项目根目录，并运行：  
```commandline
docker stack deploy -c online.yml dyezweb
```
## k3s 部署方式
部署文件格式转换：  
```commandline
docker stack deploy -c online.yml dyezweb
```