#coding=utf-8
#Version:python3.6.0
#Tool:Pycharm 2017.3.2
__data__ = ' 17:15'
__author__ = 'Colby' 

from django.shortcuts import render
from django.template import Template,Context,loader
from django.template.loader import get_template
from django.http import HttpResponse,Http404,JsonResponse
from django.http import FileResponse
from django.contrib.auth.models import User
from django.db import models
from django.db.utils import IntegrityError
from django.contrib.auth import authenticate, login
from ATOM.models import *
import json
import datetime
import ast
import base64
import io
import filetype
import math
from pyecharts.charts import Bar,Line3D
from pyecharts import options as opts
from example.commons import Faker

Tools_ID_list = {
    'base64':'ATOM/TOOLS/tools_base64.html/',
    'qrcode':'ATOM/TOOLS/tools_qrcode.html/',
}



def ToolsStatisticsCount():
    toolList = Tools_ID_list.keys()
    x = toolList
    y = []
    for i in x:
        y.append(findToolCountModel(i).toolCount)

    c = (
        Bar()
        # .add_xaxis(['1','2','3'])
        .add_xaxis(x)
        .add_yaxis('text',y)
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"))
    )
    context = dict(
        ToolCount=c.render_embed()
        # host=REMOTE_HOST,#<-----修改为这个
        # script_list=l3d.get_js_dependencies()
    )
    return context

Tools_render_ID_list = {
    'statistic':{'html':'ATOM/TOOLS/tools_statistic.html/','context':ToolsStatisticsCount},
}


def toolsHome(request):

    return render(request, 'ATOM/TOOLS/tools_home.html/')

def toolsID(request,IDName):
    # print('IDName is -> ' + IDName)
    if IDName in Tools_ID_list:
        retHtml = Tools_ID_list[IDName]
    elif IDName in Tools_render_ID_list:
        retHtml = Tools_render_ID_list[IDName]['html']
        context = Tools_render_ID_list[IDName]['context']()
        template = loader.get_template(retHtml)
        return HttpResponse(template.render(context, request))
    else :
        retHtml = 'ATOM/404.html/'
    return render(request,retHtml )

#-------------工具view----------------
#--------------base-------------------

#为tool模型增加使用次数
#@toolID:工具名 @addCount:添加或减少的使用次数
def toolCountadd(toolID,addCount):
    if toolID in Tools_ID_list:
        toolCM = findToolCountModel(toolID)
        toolCM.toolCount = toolCM.toolCount + addCount
        toolCM.save()

#返回模型对象,没有的话重新创建一个
def findToolCountModel(toolID):
    try:
        toolCM = toolUseCount.objects.get(toolID=toolID)
    except toolUseCount.DoesNotExist:
        toolCM = toolUseCount(toolID=toolID,toolCount=0)
        toolCM.save()
    return toolCM

#-------------base end---------------
#-------------base64-----------------
def base64_pro(request):
    whatType = request.POST.get("what")
    strCode = ''
    print(whatType)
    if whatType == "encode":
        whatfileType = request.POST.get("fileType")
        # print(whatfileType)
        if whatfileType == '0':#编码字符串
            # print('编码str')
            str = request.POST.get("text")
            code = base64.b64encode(str.encode('utf-8'))
            strCode = bytes.decode(code)
        elif whatfileType == '1':#编码图片
            print('编码图片')
            img = request.FILES.get("img")
            base64_data = base64.b64encode(img.read())
            code = base64_data.decode() #解码成UTF-8
            strCode = code
        elif whatfileType == '2':#编码文件
            print('编码图片')
            file = request.FILES.get("file")
            base64_data = base64.b64encode(file.read())
            code = base64_data.decode() #解码成UTF-8
            strCode = code
        toolCountadd('base64',1)
        return HttpResponse(strCode)
    elif whatType == "decode":  #解码
        whatfileType = request.POST.get("fileType")
        # 解码字符串
        if whatfileType == "0":
            code = request.POST.get("code")
            Bdata = base64.b64decode(code)
            code = Bdata.decode()  # 解码成UTF-8
            print(type(code))
            return HttpResponse(json.dumps({"fileType": "0","state":"true","data":code}, ensure_ascii=False))

        # 解码图片
        elif whatfileType == "1":
            print('decode 1')
            code = request.POST.get("code")
            Bdata = base64.b64decode(code)
            # print(type(Bdata))
            myFiletype = checkFileType(Bdata)
            if "image" in myFiletype:#先判断文件类形,是否为图片
                fileName = "static/tool/tmp/base64_tmp." + myFiletype.split('/')[-1]
                print("fileName is -> " + fileName)
                n = open(fileName, 'wb')
                # for i in img.chunks():
                n.write(Bdata)
                n.close()
                return HttpResponse(json.dumps({
                    "fileType": "1","state":"true","data":"/"+fileName,
                    "fileName":fileName.split('/')[-1]}, ensure_ascii=False))
            else:
                return HttpResponse(json.dumps({
                    "fileType": "1","state":"false","data":"false"}, ensure_ascii=False))

        # 解码文件
        elif whatfileType == "2":
            print('decode 2')
            code = request.POST.get("code")
            Bdata = base64.b64decode(code)
            # print(Bdata)
            # print(type(Bdata))
            myFiletype = checkFileType(Bdata)
            if myFiletype:  #已知文件类型
                fileName = "static/img/tmp/base64_tmp." + myFiletype.split('/')[-1]
                n = open(fileName, 'wb')
                n.write(Bdata)
                n.close()
                return HttpResponse(
                    json.dumps({"fileType": "2", "state": "true", "data": "/" + fileName,
                                "fileName":fileName.split('/')[-1]},ensure_ascii=False))
            else:
                return HttpResponse(
                    json.dumps({"fileType": "2", "state": "false", "data": "false"}, ensure_ascii=False))
        return HttpResponse()


def checkFileType(Bdata):   #bug(无法处理文本文件)
    kind = filetype.guess(Bdata)

    if kind is None:
        print('Cannot guess file type!')
        return False
    print('File extension: %s' % kind.extension)
    print('File MIME type: %s' % kind.mime)
    return kind.mime
#-------------base64-----------------end
#-------------Statistic--------------start
# def Statistic_pro():

#-------------Statistic--------------end
#-------------qrcode-----------------start
# def qrcode_pro(request):
#-------------qrcode-----------------start