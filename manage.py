#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dyezweb.settings')
    # 对于 manage.py，通常在开发环境下执行，因此将这里的 DJANGO_SETTINGS_MODULE 的值改为
    # dyezweb.settings.local，这样运行开发服务器时 django 会加载
    # dyezweb / settings / local.py 这个配置文件。
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dyezweb.settings.local')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
