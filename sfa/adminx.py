import xadmin
from xadmin import views
from .models import *




# admin models

class CustomerInfoAdmin(object):
    """客户信息管理"""
    # list_display_links = ("job_number",)  #:显示修改或查看数据详情连接的列
    show_detail_fields = ['company']  # 在指定的字段后添加一个显示数据详情的一个按钮
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ['company', 'industry', "category", "business", "phone", "introduce", "website", "remark", ]
    list_filter = ['industry', "category"]
    search_fields = ['company', ]
    ordering = ['-nid']
    model_icon = 'fa fa-cog'


class CategoryAdmin(object):
    """客户分类"""
    # list_display_links = ("job_number",)  #:显示修改或查看数据详情连接的列
    show_detail_fields = ['caption']  # 在指定的字段后添加一个显示数据详情的一个按钮
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ['caption', ]
    list_filter = ['caption', "caption"]
    search_fields = ['caption', ]
    ordering = ['-nid']
    model_icon = 'fa fa-cog'


xadmin.site.register(CustomerInfo, CustomerInfoAdmin)
xadmin.site.register(CustomerCategory,CategoryAdmin)




