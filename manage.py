"""
Django提供的一个管理工具，可以同步数据库等等

是一个命令行实用脚本，可以通过不同的方式与 Django 项目交互。这个文件的详细说明参
见 Django Project 网站
"""

#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ALHome.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
