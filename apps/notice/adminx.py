# -*- coding: utf-8 -*-
"""
@Author: Lee
@Date  : 2018/11/21 12:31
"""
import xadmin
from xadmin import views
from .models import *


class NoticeAdmin(object):
    """员工后台管理"""
    # list_display_links = ("",)  #:显示修改或查看数据详情连接的列
    show_detail_fields = ['notice_title']  # 在指定的字段后添加一个显示数据详情的一个按钮
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ['notice_title','notice_body',"notice_status","notice_url","notice_type",'notice_time',"user"]
    list_filter = ['notice_title','notice_body',"notice_status","notice_url","notice_type",'notice_time',"user"]
    search_fields = ['notice_status', 'notice_status',]
    ordering = ['-notice_time']
    model_icon = 'fa fa-user'

# settings

#  admin models

xadmin.site.register(Notice, NoticeAdmin)

