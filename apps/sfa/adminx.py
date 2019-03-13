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



class CustomerAttachAdmin(object):
    """客户附件"""
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ['customer', 'attachment', "name", "description" ]
    ordering = ['-nid']
    model_icon = 'fa fa-cog'


class CustomerLicenceAdmin(object):
    """客户营业执照"""
    # list_display_links = ("company",)  #:显示修改或查看数据详情连接的列
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ['customer', 'photo', "name",]
    ordering = ['-nid']
    model_icon = 'fa fa-cog'


class CustomerPhotoAdmin(object):
    """客户照片"""
    # list_display_links = ("company",)  #:显示修改或查看数据详情连接的列
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ['customer', 'photo', "name",]
    ordering = ['-nid']
    model_icon = 'fa fa-cog'


class CustomerLinkmanAdmin(object):
    """客户联系人管理"""
    # list_display_links = ("company",)  #:显示修改或查看数据详情连接的列
    show_detail_fields = ['name']  # 在指定的字段后添加一个显示数据详情的一个按钮
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ['customer', 'name', "gender", "job_title", "mobile", "native_place", "remark", ]
    list_filter = ['customer', ]
    search_fields = ['customer', ]
    ordering = ['-nid']
    model_icon = 'fa fa-cog'


class CustomerLinkmanAttachAdmin(object):
    """客户联系人附件"""
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ['linkman', 'attachment', "name", "description" ]
    ordering = ['-nid']
    model_icon = 'fa fa-cog'


class CustomerLinkmanCardAdmin(object):
    """客户联系人卡片"""
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ['linkman', 'photo', "name", ]
    ordering = ['-nid']
    model_icon = 'fa fa-cog'


class CustomerLinkmanPhotoAdmin(object):
    """客户联系人照片"""
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ['linkman', 'photo', "name", ]
    ordering = ['-nid']
    model_icon = 'fa fa-cog'


class CustomerMemoAdmin(object):
    """客户备忘"""
    show_detail_fields = ['title']  # 在指定的字段后添加一个显示数据详情的一个按钮
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ['customer',"title","detail" ,"recorder"]
    list_filter = ['customer', ]
    search_fields = ['customer', ]
    ordering = ['-nid']
    model_icon = 'fa fa-cog'


class CustomerMemoAttachAdmin(object):
    """客户备忘附件"""
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ['memo', 'attachment', "name", "description" ]
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
    """客户意向分类"""
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



class CustomerFollowAttachAdmin(object):
    """客户跟进附件"""
    # list_display_links = ("company",)  #:显示修改或查看数据详情连接的列
    show_detail_fields = ['follow']  # 在指定的字段后添加一个显示数据详情的一个按钮
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ['follow', 'attachment', "name", "description" ]
    ordering = ['-nid']
    model_icon = 'fa fa-cog'


class CustomerContactAdmin(object):
    """客户来往"""
    # list_display_links = ("company",)  #:显示修改或查看数据详情连接的列
    show_detail_fields = ['nid']  # 在指定的字段后添加一个显示数据详情的一个按钮
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ["nid",'customer', 'linkman', "category", "project", "description",  "received", "receivable","pending"]
    list_filter = ['customer',"category"]
    search_fields = ['customer',"category" ]
    ordering = ['-nid']
    model_icon = 'fa fa-cog'


class ContactAttachAdmin(object):
    """客户来往附件"""
    # list_display_links = ("company",)  #:显示修改或查看数据详情连接的列
    show_detail_fields = ['contact']  # 在指定的字段后添加一个显示数据详情的一个按钮
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ['contact', 'attachment', "name", "description" ]
    ordering = ['-nid']
    model_icon = 'fa fa-cog'


class SeaRuleAdmin(object):
    """公海法则"""
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ['rule',]
    list_filter = ['rule',]
    search_fields = ['rule', ]
    ordering = ['-nid']
    model_icon = 'fa fa-cog'


xadmin.site.register(CustomerInfo, CustomerInfoAdmin)
xadmin.site.register(CustomerFollow, CustomerFollowAdmin)
xadmin.site.register(CustomerLinkman, CustomerLinkmanAdmin)
xadmin.site.register(CustomerContact, CustomerContactAdmin)
xadmin.site.register(CustomerMemo, CustomerMemoAdmin)
xadmin.site.register(CustomerCategory,CategoryAdmin)
xadmin.site.register(FollowWay, FollowWayAdmin)
xadmin.site.register(FollowContact, FollowContactAdmin)

xadmin.site.register(FollowResult,FollowResultAdmin)
xadmin.site.register(CustomerPurpose, CustomerPurposeAdmin)
xadmin.site.register(SeaRule, SeaRuleAdmin)
xadmin.site.register(CustomerAttach, CustomerAttachAdmin)
xadmin.site.register(CustomerLicence, CustomerLicenceAdmin)
xadmin.site.register(CustomerPhoto, CustomerPhotoAdmin)
xadmin.site.register(CustomerLinkmanAttach, CustomerLinkmanAttachAdmin)
xadmin.site.register(CustomerLinkmanCard, CustomerLinkmanCardAdmin)
xadmin.site.register(CustomerLinkmanPhoto, CustomerLinkmanPhotoAdmin)
xadmin.site.register(CustomerMemoAttach, CustomerMemoAttachAdmin)
xadmin.site.register(CustomerFollowAttach, CustomerFollowAttachAdmin)
xadmin.site.register(ContactAttach, ContactAttachAdmin)





