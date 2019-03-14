# -*- coding: utf-8 -*-
"""
@Author: Lee
@Date  : 2018/11/21 12:31
"""
import xadmin
from xadmin import views
from .models import *


class ContractFollowAdmin(object):
    """合同跟进管理"""
    # list_display_links = ("",)  #:显示修改或查看数据详情连接的列
    # show_detail_fields = ['notice_title']  # 在指定的字段后添加一个显示数据详情的一个按钮
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ['contract','way',"contact","linkman","detail",'next_step',"date"]
    list_filter = ['contract',]
    search_fields = ['contract',]
    ordering = ['-date']
    model_icon = 'fa fa-user'


class ContractFollowAttachAdmin(object):
    """合同跟进附件"""
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ['follow', 'attachment', "name", "description" ]
    ordering = ['-nid']
    model_icon = 'fa fa-cog'


class FollowWayAdmin(object):
    """客户跟进方式"""
    # list_display_links = ("code",)  #:显示修改或查看数据详情连接的列
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ["content" ]
    list_filter = ["content"]
    search_fields = ["content" ]
    ordering = ['-nid']
    model_icon = 'fa fa-cog'

class FollowContactAdmin(object):
    """客户跟进方式"""
    # list_display_links = ("code",)  #:显示修改或查看数据详情连接的列
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ["content" ]
    list_filter = ["content"]
    search_fields = ["content" ]
    ordering = ['-nid']
    model_icon = 'fa fa-cog'

# settings

#  admin models


xadmin.site.register(ContractFollow, ContractFollowAdmin)
xadmin.site.register(FollowWay, FollowWayAdmin)
xadmin.site.register(FollowContact, FollowContactAdmin)

