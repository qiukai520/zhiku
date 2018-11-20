import xadmin
from xadmin import views
from .models import *




# admin models

class CustomerInfoAdmin(object):
    """客户信息管理"""
    # list_display_links = ("company",)  #:显示修改或查看数据详情连接的列
    show_detail_fields = ['company']  # 在指定的字段后添加一个显示数据详情的一个按钮
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ['company', 'industry', "category", "business", "phone", "introduce", "website", "remark", ]
    list_filter = ['industry', "category"]
    search_fields = ['company', ]
    ordering = ['-nid']
    model_icon = 'fa fa-cog'


class CategoryAdmin(object):
    """客户分类"""
    show_detail_fields = ['caption']  # 在指定的字段后添加一个显示数据详情的一个按钮
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ['caption', ]
    list_filter = ['caption', ]
    search_fields = ['caption', ]
    ordering = ['-nid']
    model_icon = 'fa fa-cog'


class FollowWayAdmin(object):
    """客户跟进方式"""
    # list_display_links = ("code",)  #:显示修改或查看数据详情连接的列
    show_detail_fields = ['code',"content"]  # 在指定的字段后添加一个显示数据详情的一个按钮
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ['code',"content" ]
    list_filter = ['code',"content"]
    search_fields = ['code',"content" ]
    ordering = ['-nid']
    model_icon = 'fa fa-cog'


class FollowContactAdmin(object):
    """客户联络方式"""
    # list_display_links = ("code",)  #:显示修改或查看数据详情连接的列
    show_detail_fields = ['code',"content"]  # 在指定的字段后添加一个显示数据详情的一个按钮
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ['code',"content" ]
    list_filter = ['code',"content"]
    search_fields = ['code',"content" ]
    ordering = ['-nid']
    model_icon = 'fa fa-cog'



class FollowResultAdmin(object):
    """客户需求意向方式"""
    # list_display_links = ("code",)  #:显示修改或查看数据详情连接的列
    show_detail_fields = ['code',"content"]  # 在指定的字段后添加一个显示数据详情的一个按钮
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ['code',"content" ]
    list_filter = ['code',"content"]
    search_fields = ['code',"content" ]
    ordering = ['-nid']
    model_icon = 'fa fa-cog'



class CustomerPurposeAdmin(object):
    """客户跟进方式"""
    # list_display_links = ("code",)  #:显示修改或查看数据详情连接的列
    show_detail_fields = ['code',"content"]  # 在指定的字段后添加一个显示数据详情的一个按钮
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ['code',"content" ]
    list_filter = ['code',"content"]
    search_fields = ['code',"content" ]
    ordering = ['-nid']
    model_icon = 'fa fa-cog'



class CustomerFollowAdmin(object):
    """客户跟进记录"""
    # list_display_links = ("company",)  #:显示修改或查看数据详情连接的列
    show_detail_fields = ['customer']  # 在指定的字段后添加一个显示数据详情的一个按钮
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ['customer', 'way', "contact", "linkman", "result",  "next_step", ]
    list_filter = ['customer',]
    search_fields = ['customer', ]
    ordering = ['-nid']
    model_icon = 'fa fa-cog'


xadmin.site.register(CustomerCategory,CategoryAdmin)
xadmin.site.register(CustomerInfo, CustomerInfoAdmin)
xadmin.site.register(CustomerFollow, CustomerFollowAdmin)
xadmin.site.register(FollowWay, FollowWayAdmin)
xadmin.site.register(FollowContact, FollowContactAdmin)
xadmin.site.register(FollowResult,FollowResultAdmin)
xadmin.site.register(CustomerPurpose, CustomerPurposeAdmin)








