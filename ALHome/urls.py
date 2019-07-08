"""ALHome URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

    表示web工程Url映射的配置
"""

from django.contrib import admin
from django.conf.urls import url,include
from django.urls import path
# from ATOM.views import hello,current_datetime,current_datetime_t1,current_datetime_t2,hours_ahead
# from ATOM.views import *

from ATOM.view import user_view
from ATOM.view import main_view
from ATOM.view import blog_view
from ATOM.view import tools_view
from ATOM.view.main_view import *

urlpatterns = [
    #main url
    path('admin/', admin.site.urls),
    # path(r'', hello),
    # path(r'^admin/', include(admin.site.urls)),
    path(r'ATOM/',main_view.atom_home ),
    path(r'ATOM_home.html/',main_view.atom_home ),
    path(r'ATOM/CV/cv_home.html/',CV_home ),
    path(r'ATOM/404.html/',atom_404 ),

    path(r'ATOM/CV/cv_allBlog.html/',CV_allBlog ),
    path(r'ATOM/CV/cv_dissertation.html/',CV_dissertation ),
    path(r'ATOM/CV/blog/<int:blogID>/',blog_view.blog),
    path(r'ATOM/blog_tag/<str:tagName>/',blog_view.tagName),
    path(r'getBlogInfo/',blog_view.getBlogInfo),
    path(r'getEyeCount/',blog_view.getEyeCount),
    #atom Tools view
    path(r'ATOM/TOOLS/tools_home.html/',tools_view.toolsHome ),
    path(r'ATOM/TOOLS/tools_ID/<str:IDName>/',tools_view.toolsID ),
    path(r'tools/base64/', tools_view.base64_pro),
    path(r'tools/qrcode/', tools_view.qrcode_pro),



    #注册/登录
    path(r'login/',user_view.login),
    path(r'ATOM/user/user_info.html',user_view.user_info),
    path(r'changeHeadIcon/',user_view.changeHeadIcon),

    # path(r'time/', current_datetime_t2),              # r表示原始字符串,不转义
    # url(r'^time/plus/(\d+)/$', hours_ahead),   #(参数) 将被传到hours_ahead()函数的第二个变量
    #--------------------


]
