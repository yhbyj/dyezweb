# _*_ coding: utf-8 _*_
__author__ = 'Yang Haibo'
__date__ = '2020/5/21 9:51'

from fabric import Connection

from _credentials import *


def deploy(c):
    supervisor_conf_path = '~/etc/'
    supervisor_program_name = 'dyezweb'

    project_root_path = '~/projects/dyezweb/'

    # 先停止应用
    with c.cd(supervisor_conf_path):
        cmd = '~/.local/bin/supervisorctl stop {}'.format(supervisor_program_name)
        c.run(cmd)

    with c.cd(project_root_path):
        # 本地库会发生改变，强制合并
        c.run('git reset --hard')
        c.run('git pull')
        c.run('cp _deployment/legacy/online/requirements_extra.txt ./')

    # 上传覆盖配置文件
    c.put('settings.py', '/home/yhb/projects/dyezweb/dyezweb')

    # 进入项目根目录，安装依赖包，迁移数据库，收集静态文件等
    with c.cd(project_root_path):
        with c.prefix('workon dyezweb'):
            c.run('pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple')
            c.run('pip install -r requirements_extra.txt -i https://mirrors.aliyun.com/pypi/simple')
            c.run('python manage.py migrate')
            c.run('python manage.py collectstatic --noinput')

    # 重新启动应用
    with c.cd(supervisor_conf_path):
        cmd = '~/.local/bin/supervisorctl start {}'.format(supervisor_program_name)
        c.run(cmd)


if __name__ == '__main__':
    HOST = SSH_HOST
    USERNAME = SSH_USERNAME
    PORT = 22
    PASSWORD = SSH_PASSWORD
    c = Connection(host=HOST, user=USERNAME, port=PORT, connect_kwargs={'password': PASSWORD})
    deploy(c)