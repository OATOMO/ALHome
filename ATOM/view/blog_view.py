#coding=utf-8
#Version:python3.6.0
#Tool:Pycharm 2017.3.2
__data__ = ' 22:49'
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
import ast




def blog(request,blogID):   #按照blog ID返回html
    print(blogID)
    # if(blogID==0):
    #     return render(request, 'BLOG/blog_template.html')
    # elif(blogID==1):
    #     return render(request, 'CV/BLOG/blog_Harris_new.html')
    html_json = getBlogId(blogID)
    html = html_json["path"]
    print (html)
    return render(request, html)

def tagName(request,tagName): #按照tag返回 搜索到的相关文章 渲染返回页面
    tagNameList = getTagNameList_infoList(tagName,"list")
    tagInfoList = getTagNameList_infoList(tagName,"infoList")
    print(tagNameList)
    return render(request, "ATOM/CV/BLOG/cv_selectTag.html",{'tagInfoList':tagInfoList})

def getTagNameList_infoList(tagName,type):#获取想寻找的tag 列表
    with open('templates/blog_list.txt', encoding='utf-8') as f:
        temp_list = json.loads(f.read())
        f.close()
        if type == "list":
            tagNameList=[]
            # print (temp_list.keys())
            for i in temp_list.keys():
                if tagName in temp_list[i]['tag']:
                    tagNameList.append(i)
            return tagNameList  #只返回ID名列表
        elif type == "infoList":
            tagInfoList=[]
            for i in temp_list.keys():
                if tagName in temp_list[i]['tag']:
                    temp = {}
                    temp["id"] = i
                    temp["url"] = temp_list[i]['url']
                    temp["tag"] = temp_list[i]['tag']
                    temp["date"] = temp_list[i]['date']
                    temp["title"] = temp_list[i]['title']
                    temp["description"] = temp_list[i]['description']
                    tagInfoList.append(temp)
            return tagInfoList  #返回字典信息列表
#id@int type
def getBlogId(id):
    with open('templates/blog_list.txt', encoding='utf-8') as f:
        temp_list = json.loads(f.read())
        f.close()
        # print(temp_list["ID"+"2"][0])
        return temp_list["ID"+str(id)]

def getBlogNumber():
    with open('templates/blog_list.txt', encoding='utf-8') as f:
        temp_list = json.loads(f.read())
        f.close()
        blogIDList = temp_list.keys()
        validBlogIDList = []
        validBlogIDDict = {}
        for i in blogIDList:
            if temp_list[i]["date"] != "":
                validBlogIDList.append(i)
                validBlogIDDict[i] = temp_list[i]
            # print (temp_list[i]["date"])

        # print (temp_list)
        # print (len(temp_list))#所以列表数
        # # print (blogIDList)
        # print (validBlogIDList)
        # print (len(validBlogIDList))#有效列表数
        # print (validBlogIDDict)
        # print (len(validBlogIDDict))
        #end def getBlogNumber()
        result = validBlogIDDict
        return result


def getBlogInfo(request):
    if request.method == "POST":
        whatType = request.POST.get("what")
        if whatType == "getBlogPage":
            result = getBlogNumber()
            return HttpResponse(json.dumps(result, ensure_ascii=False))
    return HttpResponse("")

#向页面返回点赞信息
def getEyeCount(request):
    if request.method == "POST":
        whatType = request.POST.get("what")
        if whatType == "getEyeCount":
            mUrl = request.POST.get("blogUrl")
            mBlogID = getIdInUrl(mUrl)
            result = __getEyeCount(mBlogID,request)
            eyeCountAdd(mBlogID,1)
            return HttpResponse(HttpResponse(json.dumps(result, ensure_ascii=False)))
        elif whatType == "getAddHeart":
            mUrl = request.POST.get("blogUrl")
            mBlogID = getIdInUrl(mUrl)
            heartCountAdd(mBlogID)
            return HttpResponse("OK")
        elif whatType == "getAddStar":
            mUrl = request.POST.get("blogUrl")
            mBlogID = getIdInUrl(mUrl)
            # heartCountAdd(mBlogID)
            #从session拿到用户信息
            m_userName = request.session.get("userName")
            m_login_state = request.session.get("loginState")
            if (m_login_state != "activate"):#没登录的话
                result = 'nonactivated'
            else:
                result = starCountAdd(mBlogID,m_userName)

            return HttpResponse(result)

def __getUserInfo(m_userName):
    try:
        m_userInfo = userInfo.objects.get(userName=m_userName)
        return m_userInfo
    except userInfo.DoesNotExist:
        m_userInfo = userInfo()
        return m_userInfo

def starCountAdd(mBlogID,m_userName):
    m_userInfo = __getUserInfo(m_userName)
    if m_userInfo != None:#有这个用户的话,为这个用户添加收藏
        m_userStarID_raw = m_userInfo.userStarID
        if m_userStarID_raw == None or m_userStarID_raw == '':
            m_userStarID_raw = "[]"
            m_userInfo.userStarID = "[]"
            m_userInfo.save()
        starList = eval(m_userStarID_raw)
        if mBlogID in starList:#已收藏 为文章收藏 与 用户 减一
            starList.remove(mBlogID)
            m_userStarID = json.dumps(starList, ensure_ascii=False)
            m_userInfo.userStarID = m_userStarID#为用户去除此收藏
            m_userInfo.save()
            mEyeCountModel = __getEyeCountModel(mBlogID)
            mEyeCountModel.starCount = mEyeCountModel.starCount - 1
            mEyeCountModel.save()
            return "hasStat"
        else:#未收藏 为文章收藏 与 用户 加一
            starList.append(mBlogID)
            # m_userStarID = (",".join(starList))
            #为用户添加收藏的blogID
            m_userStarID = json.dumps(starList, ensure_ascii=False)
            m_userInfo.userStarID = m_userStarID
            m_userInfo.save()
            # print (m_userStarID)
            mEyeCountModel = __getEyeCountModel(mBlogID)
            mEyeCountModel.starCount = mEyeCountModel.starCount + 1
            mEyeCountModel.save()
            return "OK"

#判断用户是否收藏blogID
def isStar(mBlogID,m_userName):
    m_userInfo = __getUserInfo(m_userName)
    m_userStarID_raw = m_userInfo.userStarID    #从用户信息模型中获取收藏ID的json字符串
    starList = eval(m_userStarID_raw)           #将收藏ID的json字符串解析为列表
    if mBlogID in starList:  # 已收藏
        result = True
    else:
        result = False
    return result

def eyeCountAdd(mBlogID,number=1):
    mEyeCountModel = __getEyeCountModel(mBlogID)
    mEyeCountModel.eyeCount = mEyeCountModel.eyeCount+number
    mEyeCountModel.save()

def heartCountAdd(mBlogID):
    mEyeCountModel = __getEyeCountModel(mBlogID)
    mEyeCountModel.heartCount = mEyeCountModel.heartCount+1
    mEyeCountModel.save()

def getIdInUrl(mUrl):
    mUrlList =  mUrl.split('/')
    result = ""
    for item in mUrlList:
        if item.isdigit():
            result = "ID"+item
    return result

def __getEyeCountModel(mBlogID):
    try:
        print("找到")
        mEyeCountModel = eyeCountModel.objects.get(blogID=mBlogID)
        return mEyeCountModel
    except eyeCountModel.DoesNotExist:
        print("创建")
        mEyeCountModel = eyeCountModel(blogID=mBlogID,eyeCount=0,
                                       heartCount=0,starCount=0)
        return mEyeCountModel

#从模型中获取点赞信息
def __getEyeCount(mBlogID,request):
    mEyeCountModel = __getEyeCountModel(mBlogID)
    m_userName = request.session.get("userName")
    m_login_state = request.session.get("loginState")
    if (m_login_state != "activate"):  # 没登录的话 不判断直接 False
        starStatic = False
    else:   # 登录的话判断一下用户是否收藏
        starStatic = isStar(mBlogID,m_userName)
    result = {}
    result['id'] = mBlogID
    result['eyeCount'] = mEyeCountModel.eyeCount
    result['heartCount'] = mEyeCountModel.heartCount
    result['starCount'] = mEyeCountModel.starCount
    result['result'] = 'OK'
    result['starStatic'] = starStatic   #该账户是否已收藏此文章
    return result

