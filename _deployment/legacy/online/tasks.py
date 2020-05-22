# _*_ coding: utf-8 _*_
__author__ = 'Yang Haibo'
__date__ = '2020/5/22 7:59'

# from fabric import task

# invoke --list
# invoke deploy
# 系统找不到指定的路径。

from invoke import task, Responder

from _credentials import github_password, github_username


def _get_github_auth_responders():
    """
    返回 GitHub 用户名密码自动填充器
    """
    username_responder = Responder(
        pattern="Username for 'https://github.com':",
        response='{}\n'.format(github_username)
    )
    password_responder = Responder(
        pattern="Password for 'https://{}@github.com':".format(github_username),
        response='{}\n'.format(github_password)
    )
    return [username_responder, password_responder]


@task()
def deploy(c):
    supervisor_conf_path = '~/etc/'
    supervisor_program_name = 'dyezweb'

    project_root_path = '~/projects/dyezweb/'
    project_settings_path = '~/projects/dyezweb/dyezweb'

    # 先停止应用
    with c.cd(supervisor_conf_path):
        cmd = '~/.local/bin/supervisorctl stop {}'.format(supervisor_program_name)
        c.run(cmd)

    with c.cd(project_root_path):
        cmd = 'git pull'
        responders = _get_github_auth_responders()
        c.run(cmd, watchers=responders)
        c.run('cp _deployment/legacy/online/requirements_extra.txt ./')

    # 进入项目的配置文件目录，上传覆盖配置文件
    with c.cd(project_settings_path):
        c.put('settings.py')

    # 进入项目根目录，安装依赖包，迁移数据库，收集静态文件等
    with c.cd(project_root_path):
        # c.run('~/.virtualenvs/dyezweb/bin/pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple')
        with c.prefix('workon dyezweb'):
            c.run('pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple')
            c.run('pip install -r requirements_extra.txt -i https://mirrors.aliyun.com/pypi/simple')
            c.run('python manage.py migrate')
            c.run('python manage.py collectstatic --noinput')

    # 重新启动应用
    with c.cd(supervisor_conf_path):
        cmd = '~/.local/bin/supervisorctl start {}'.format(supervisor_program_name)
        c.run(cmd)