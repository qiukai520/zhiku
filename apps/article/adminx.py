# -*- coding: utf-8 -*-
"""
@Author: Lee
@Date  : 2018/12/3 12:03
"""

import xadmin
# Register your models here.

from .models import *

class PostsAdmin(object):
    list_display = ( 'title','author2', 'created_time')    # 指定后台显示的字段
    search_fields = ( 'title','author2','created_time')    # 增加搜索框
    list_filter = ( 'title','author2', 'created_time')     # 高级筛选
    show_detail_fields = ['title']                       # 显示预览功能
    # style_fields = {"content2": "ueditor"}
    model_icon = 'fa fa-cog'


xadmin.site.register(Posts, PostsAdmin)
