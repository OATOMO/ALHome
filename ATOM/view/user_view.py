#coding=utf-8
#Version:python3.6.0
#Tool:Pycharm 2017.3.2
__data__ = ' 22:42'
__author__ = 'Colby' 

from django.shortcuts import render
from django.template import Template,Context
from django.template.loader import get_template
from django.http import HttpResponse,Http404
from django.contrib.auth.models import User
from django.db import models
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate, login
from ATOM.models import *
import json
import datetime

def login(request):
    # print(request.GET)
    whatType = request.GET.get("what")
    if whatType == "login":     #注册
        m_userName = request.GET.get("user")
        m_password = request.GET.get("password")
        m_email = request.GET.get("email")
        m_gender = request.GET.get("gender")

        print("m_m_gender : " + str(m_gender))
        print(m_gender)

        try:                            #get()不报错说明用户名存在
            m_user = User.objects.get(username=m_userName)
            # print("用户名已被使用 NO")
            return HttpResponse("注册失败,用户已被使用")
        except User.DoesNotExist:       #报错说明get()不到用户名,用户名可以使用
            # print("用户名已被可以使用 OK")
            m_user = User.objects.create_user(username=m_userName, password=m_password, email=m_email)
            m_userInfo = userInfo(userName=m_userName,
                                  userHeadIconPath="",
                                  userGender=m_gender,
                                  user=m_user).save()
            return HttpResponse("True")
    elif whatType == "userCheck":   #检查用户名是否重复
        m_user = request.GET.get("userName")
        try:
            user = User.objects.get(username=m_user)
            print("用户名已被使用 NO")
            return HttpResponse("用户名已被使用")
        except User.DoesNotExist:
            print("用户名已被可以使用 OK")
            return HttpResponse("OK")
    elif whatType == "logup":   #登录
        m_userName = request.GET.get("userName")
        m_password = request.GET.get("password")
        user = authenticate(username=m_userName, password=m_password)
        if user is not None:
            if user.is_active:
                #登录成功
                print("登录成功")
                initUserSession(request,m_userName)
                return HttpResponse("登录成功")
            else:
                print("登录失败")
                return HttpResponse("登录失败")
        else:
            print("登录失败")
            return HttpResponse("登录失败")
    elif whatType == "autoLogin":   #自动登录(session)
        print("activate autoLogin")
        m_userName = request.session.get("userName")
        m_login_state = request.session.get("loginState")
        if(m_login_state == "activate"):
            print("已登录")
            result = {"status":"activate","userName":m_userName}
            return HttpResponse(json.dumps(result,ensure_ascii=False))
        else:
            print("没登录")
            result = {"status": "nonactivated", "userName": m_userName}
            return HttpResponse(json.dumps(result, ensure_ascii=False))
    elif whatType == "logout":   #注销
        # del request.session["user_info"]
        # del request.session["login_state"]
        request.session.flush()
        return HttpResponse("logout")
    elif whatType == "getHeadIcon":
        m_userName = request.GET.get("userName")
        return HttpResponse(findUserHeadIcon(m_userName))
    elif whatType == "getUserInfo":
        print("getUserInfo")
        # m_userName = request.session.get("userName")
        # m_login_state = request.session.get("loginState")
        m_user_info = _get_userInfo(request)
        if (m_user_info["status"] == "activate"):
            print("已登录")
            # result = {"status": "activate", "userName": m_userName}
            result = m_user_info
            return HttpResponse(json.dumps(result, ensure_ascii=False))
        else:
            print("没登录")
            result = {"status": "nonactivated", "userName": m_user_info["userName"]}
            return HttpResponse(json.dumps(result, ensure_ascii=False))

def _get_userInfo(request):
    m_userName = request.session.get("userName")    #查看已登录的用户名
    m_login_state = request.session.get("loginState")
    m_user_info = {}                                #创建用户信息字典
    m_user_info["status"] = m_login_state           #填入状态
    m_user_info["userName"] = m_userName            #填入用户名
    m_user_info["headIconPath"] = findUserHeadIcon(m_userName)  #填入用户头像路径
    m_user_info["email"] = getEmail(m_userName)     #填入邮箱
    return m_user_info

def getEmail(userName):
    try:
        m_user = userInfo.objects.get(username=userName)
        m_email = m_user.email
    except User.DoesNotExist:
        m_email = ""
    return m_email

def findUserHeadIcon(userName):
    try:    #尝试获取用户头像
        m_userinfo = userInfo.objects.get(userName=userName)#存用户头像时,存到/static/img/headIcon/用户名.png
        m_headIconPath = m_userinfo.userHeadIconPath
        if m_headIconPath == "":
            if m_userinfo.userGender == "man":
                path = "/static/img/headIcon/man.png"
            elif m_userinfo.userGender == "woman":
                path ="/static/img/headIcon/woman.png"
            return path
        else:
            return m_userinfo.userHeadIconPath
    except userInfo.DoesNotExist:
        m_user = User.objects.get(username=userName)
        m_userinfo = userInfo(userName=userName,userHeadIconPath = "/static/img/headIcon/man2.png",
                              userGender="man",user=m_user,userStarID="[]")
        m_userinfo.save()
        return "/static/img/headIcon/man2.png"



def initUserSession(request,userName):
    request.session["userName"] = userName
    request.session["loginState"] = "activate"

def user_info(request): #用户中心视图
    return render(request, 'ATOM/user/user_info.html')

def changeHeadIcon(request):
    if request.method == "POST":
        img = request.FILES.get('img')
        m_userName = request.POST.get('userName')
        # img是个对象（文件大小，文件名称，文件内容...）
        print(img.name)
        print(img.size)
        fileName = "./static/img/headIcon/user/"+ m_userName + "." + img.name.split('.')[-1]
        print (fileName)
        n = open(fileName, 'wb')
        for i in img.chunks():
            n.write(i)
        n.close()
        return HttpResponse('修改成功')