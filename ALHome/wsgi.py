#coding=utf-8"""
"""
WSGI config for ALHome project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/

是兼容 WSGI 的 Web 服务器的入口点，用于伺服项目
"""

import os
import sys
from django.core.wsgi import get_wsgi_application




sys.path.append('/usr/lib/python2.7/site-packages')
sys.path.append('/usr/lib64/python2.7/site-packages')
sys.path.append('/usr/lib/python3.5/site-packages')
sys.path.append('/usr/lib64/python3.5/site-packages')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ALHome.settings')

application = get_wsgi_application()
