#coding=utf-8
#Version:python3.6.0
#Tool:Pycharm 2017.3.2
__data__ = ' 17:15'
__author__ = 'Colby' 

from django.shortcuts import render
from django.template import Template,Context,loader
from django.template.loader import get_template
from django.http import HttpResponse,Http404
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
}

def line3d():
    _data = []
    for t in range(0, 25000):
        _t = t / 1000
        x = (1 + 0.25 * math.cos(75 * _t)) * math.cos(_t)
        y = (1 + 0.25 * math.cos(75 * _t)) * math.sin(_t)
        z = _t + 2.0 * math.sin(75 * _t)
        _data.append([x, y, z])
    c = (
        Line3D()
            .add(
            "",
            _data,
            xaxis3d_opts=opts.Axis3DOpts(Faker.clock, type_="value"),
            yaxis3d_opts=opts.Axis3DOpts(Faker.week_en, type_="value"),
            grid3d_opts=opts.Grid3DOpts(width=100, height=100, depth=100),
        )
            .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(
                max_=30, min_=0, range_color=Faker.visual_color
            ),
            title_opts=opts.TitleOpts(title="Line3D-基本示例"),
        )
    )
    return c

def ToolsStatisticsCount():
    c = (
        Bar()
        .add_xaxis(['1','2','3'])
        .add_yaxis('text',[5,6,7])
        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-基本示例", subtitle="我是副标题"))
    )
    return c

def toolsHome(request):
    template = loader.get_template('ATOM/TOOLS/tools_home.html/')
    myBar = ToolsStatisticsCount()
    context = dict(
        myechart=myBar.render_embed()
        # host=REMOTE_HOST,#<-----修改为这个
        # script_list=l3d.get_js_dependencies()
    )

    return HttpResponse(template.render(context, request))
    # return render(request, 'ATOM/TOOLS/tools_home.html/')

def toolsID(request,IDName):
    # print('IDName is -> ' + IDName)
    if IDName in Tools_ID_list:
        retHtml = Tools_ID_list[IDName]
    else :
        retHtml = 'ATOM/404.html/'
    return render(request,retHtml )

#-------------工具view----------------
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
        return HttpResponse(strCode)
    elif whatType == "decode":  #解码
        code = request.POST.get("code")
        Bdata = base64.b64decode(code)
        print(Bdata)
        print(type(Bdata))
        myFiletype = checkFileType(Bdata)
        if myFiletype:#先判断文件类行,都不是的话视为str
            response = FileResponse(Bdata)
            # response['Content-Type'] = myFiletype
            # response['Content-Disposition'] = 'attachment;filename="example.tar.gz"'
            return response
        return FileResponse()


def checkFileType(Bdata):   #bug(无法处理文本文件)
    kind = filetype.guess(Bdata)

    if kind is None:
        print('Cannot guess file type!')
        return False
    print('File extension: %s' % kind.extension)
    print('File MIME type: %s' % kind.mime)
    return kind.mime
#-------------base64-----------------end