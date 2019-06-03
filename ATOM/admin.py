from django.contrib import admin
from .models import *
# Register your models here.
class postAdmin(admin.ModelAdmin):
    #定制注册模型
    list_display = ('title','slug','author','publish','status')#定义要显示的字段
    list_filter = ('status','created','publish')#右侧过滤菜单
    search_fields = ('title','body')#搜索框设置(根据什么字段搜索)
    prepopulated_fields = {'slug':('title',)}#填充
    raw_id_fields = ('author',)#搜索插件
    date_hierarchy = 'publish' #时间导航栏
    ordering = ['status','publish']#排序字段

admin.site.register(post,postAdmin)
admin.site.register(IMG)
admin.site.register(userInfo)
admin.site.register(eyeCountModel)
