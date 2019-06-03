#coding=utf-8
#Version:python3.6.0
#Tool:Pycharm 2017.3.2
__data__ = ' 22:42'
__author__ = 'Colby' 
# Create your views here.
from django.shortcuts import render
from django.template import Template,Context
from django.template.loader import get_template
from django.http import HttpResponse,Http404
from django.contrib.auth.models import User
from django.db import models
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate, login
import json
import datetime

def hello(request):
    return HttpResponse("Hello world")

def current_datetime(request):
    now = datetime.datetime.now()
    html = "It is now : " + str(now)
    return HttpResponse(html)

def current_datetime_t1(request):   #试试Template
    now = datetime.datetime.now()
    t = Template("<html><body>It is now {{ current_date }}.</body></html>")
    print(type(t))
    html = t.render(Context({'current_date':now}))
    return HttpResponse(html)

def current_datetime_t2(request):   #试试Template
    now = datetime.datetime.now()
    t = get_template('current_datetime.html')
    # print(type(t))
    html = t.render({'current_date':now})
    return HttpResponse(html)
    # return render(request, 'current_datetime.html', {'current_date': now})

def hours_ahead(request,offset):        #offset,由()号正则表达式匹配到传递过来
    assert False
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = "It is now : " + str(dt)
    return HttpResponse(html)

def atom_home(request):
    return render(request, 'ATOM_home.html')
    # return HttpResponse("ATOM")

def CV_home(request):
    return render(request, 'CV/cv_home.html')

def CV_allBlog(request):
    return render(request, 'CV/cv_allBlog.html')

def CV_dissertation(request):
    return render(request, 'CV/cv_dissertation.html')

def atom_404(request):
    return render(request, '404.html')