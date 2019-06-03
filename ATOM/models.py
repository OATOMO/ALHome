from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.
'''
    ---------------字段类型---------------
    普通字段类型:
    models.CharField()      :字符串字段,存储一些较短的字符串 
                -choices:可选的值         
    models.SlugField()      :只包含字母下划线和连字符字段
                -unique_for_date:使用日期构建Url
    models.TextField()      :大容量文本字段
    models.DateTimeField()  
    models.DateField()
                -auto_now:当该字段被保存时设置为当前时间;
                -auto_now_add:当字段首次被创建时将值设置为当前时间;
    models.TimeField()
    models.FileField()      :文件上传字段
    models.FloatField()     :浮点字段
    models.ImageField()     :
    models.PhoneField()     :号码字段
    models.UrlField()       :保存URL
    models.ForeignKey()     :外键
                -related_name:指定反向关系名称
'''


class PublishedManager(models.Manager):
    #定义模型管理器
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='published')

# 定义数据表:
#     标题:
#     标识:
#     作者:
#     内容:
#     发布时间:创建时间:更新时间;
#     状态:
class post(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250,unique_for_date='publish')
    author = models.ForeignKey(User,related_name="blog_posts",on_delete=models.CASCADE)
    body = models.TextField()
    # publish = models.DateTimeField(default=timezone.now())
    publish = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # m_file = models.FileField(null=True, blank=True)
    STATUS_CHOICES=(
        ('draft','Draft'),
        ('published','Published'),
    )
    status = models.CharField(max_length=20,
                              choices=STATUS_CHOICES,
                              default='draft')
    objects = models.Manager()
    published = PublishedManager()


    class Meta:
        '''
        在模型类的Meta子类定义元数据
            -数据库表名
            -数据库字段排序
            abstract:True or False标识本类是否为抽象的基类
            app_label:定义这个类属于的应用app_label='ATOM'
            db_table:映射数据表名,如果不指定此字段Django会自动创建(format :应用名称_模型名称)
            order_with_respect_to:定义按照某个外键的应用关系排序
            ordering:按照默认字段进行排序,默认升序

        '''
        ordering=('-publish',)
    def __str__(self):
        return self.title

class IMG(models.Model):
    img = models.ImageField(upload_to='img')
    imgName = models.CharField(max_length=40)

class userInfo(models.Model):
    userName = models.CharField(max_length=40)
    userHeadIconPath = models.CharField(max_length=40,blank=True)  #头像图片路径(图片名为 [userName_headIcon.jpg])
    userGender = models.CharField(max_length=10,blank=True) #用户性别,创建时选择
    user = models.ForeignKey(User,blank=True,default='',on_delete=models.CASCADE) #用户对象外键
    userStarID =  models.TextField(null=True,blank=True)
    #... 以后添加存储一些额外内容
    def __str__(self):
        return "info :"+self.userName

class eyeCountModel(models.Model):
    blogID = models.CharField(max_length=10)
    eyeCount = models.BigIntegerField()
    heartCount = models.BigIntegerField()
    starCount = models.BigIntegerField()
    def __str__(self):
        return "eyeCountModel -> " +self.blogID

class toolUseCount(models.Model):
    toolID = models.CharField(max_length=10)#工具名
    toolCount = models.BigIntegerField()    #base64工具总使用次数
    def __str__(self):
        return "toolUseCount -> " +self.toolID