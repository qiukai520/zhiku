from django.db import models
from datetime import datetime
# from django.contrib.auth.models import User
from rbac.models import User as User

# Create your models here.

class Posts (models.Model):
    title = models.CharField(max_length=70, verbose_name='文章标题')
    # excerpt = models.CharField(max_length=200, blank=True, verbose_name='文章摘要',help_text="输入40个字内")
    image = models.ImageField(upload_to='article/%Y/%m/%d', default='article/article.jpg',verbose_name=u"首页封面图片",max_length=200, blank=True,help_text="标准尺寸长600像素,宽200像素")
    image2 = models.ImageField(upload_to='article2/%Y/%m/%d', default='article/article.jpg',verbose_name=u"文章内容配图",max_length=200, blank=True,help_text="尺寸不限")
    content = models.TextField(verbose_name=u"文章内容", blank=True)
    # content2 = UEditorField(u'内容', width=860, height=600, toolbars="full", imagePath="article/ueditor/", filePath="article/ueditor/",
    #                        upload_settings={"imageMaxSize": 1204000},command=None, blank=True)
    author2 = models.CharField(max_length=30, verbose_name=u"作者", blank=True)
    author = models.ForeignKey(User, verbose_name='用户名', on_delete=models.CASCADE)
    # gender = models.CharField(max_length=10, choices=(("1", "保存草稿"),("2", "发布")), verbose_name=u"是否发布文章", default="2", blank=True)
    created_time = models.DateTimeField(default=datetime.now,verbose_name='创建时间')

    class Meta:

        verbose_name = u"发布文章"
        verbose_name_plural = verbose_name
        ordering = ['-created_time']           #让文章按发布时间来排序

    def __str__(self):
        return self.title