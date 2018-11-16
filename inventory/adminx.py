import xadmin
from xadmin import views
from .models import *
from django.utils.safestring import mark_safe
from django.utils.html import format_html



# admin models


class GoodsUnitAdmin(object):
    """商品单位"""
    list_display = ["caption"]
    search_fields = ['caption']
    model_icon = 'fa fa-cog'

class GoodsCategoryAdmin(object):
    """商品分类"""
    list_display = ["caption","parent"]
    search_fields = ['caption',"parent"]
    model_icon = 'fa fa-cog'


class GoodsAdmin(object):
    """供应商品"""
    # list_display_links = ("job_number",)  #:显示修改或查看数据详情连接的列
    show_detail_fields = ['name']  # 在指定的字段后添加一个显示数据详情的一个按钮
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ['name', "category", "description", "unit", "standard","start_month", "end_month","area" ]
    list_filter = ["category"]
    search_fields = ['name', ]
    ordering = ['-nid']
    model_icon = 'fa fa-cog'

class GoodsAttachAdmin(object):
    """商品附件"""
    list_display = ["goods","attachment","name", "description"]
    list_filter = ["goods"]
    search_fields = ['goods']
    model_icon = 'fa fa-cog'



class IndustryAdmin(object):
    """行业"""
    list_display = ["industry"]
    search_fields = ['industry']
    model_icon = 'fa fa-cog'


class LinkmanAdmin(object):
    """供应商联系人"""
    # list_display_links = ("job_number",)  #:显示修改或查看数据详情连接的列
    show_detail_fields = ['supplier']  # 在指定的字段后添加一个显示数据详情的一个按钮
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ['supplier','name',"gender","age","marriage","mobile","phone","birthday","native_place","delete_status"]
    list_filter = ['supplier',"gender"]
    search_fields = ['supplier', 'name',]
    ordering = ['-delete_status']
    model_icon = 'fa fa-cog'


class LinkmanAttachAdmin(object):
    """联系人附件"""
    list_display = ["linkman","attachment","name", "description"]
    list_filter = ["linkman"]
    search_fields = ['supplier']
    model_icon = 'fa fa-cog'



class LinkmanCardAdmin(object):
    """联系人名片"""
    list_display = ["linkman","photo","name", ]
    list_filter = ["linkman"]
    search_fields = ['linkman']
    model_icon = 'fa fa-cog'


class LinkmanPhotoAdmin(object):
    """联系人照片"""
    list_display = ["linkman","photo","name", ]
    list_filter = ["linkman"]
    search_fields = ['linkman']
    model_icon = 'fa fa-cog'



class IndustryAdmin(object):
    """行业"""
    list_display = ["industry"]
    search_fields = ['industry']
    model_icon = 'fa fa-cog'

# 供应商
class SupplierAdmin(object):
    """供应商后台管理"""
    # list_display_links = ("job_number",)  #:显示修改或查看数据详情连接的列
    show_detail_fields = ['company']  # 在指定的字段后添加一个显示数据详情的一个按钮
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ['company','industry',"category","products","phone","introduce","website","remark",]
    list_filter = ['industry',"category"]
    search_fields = ['company',]
    ordering = ['-nid']
    model_icon = 'fa fa-cog'


class SupplierCategoryAdmin(object):
    """供应商分类"""
    list_display = ["caption"]
    search_fields = ['caption']
    model_icon = 'fa fa-cog'


class SupplierAttachAdmin(object):
    """供应商附件"""
    list_display = ["supplier","attachment","name", "description"]
    list_filter = ["supplier"]
    search_fields = ['supplier']
    model_icon = 'fa fa-cog'


class SupplierLicenceAdmin(object):
    """供应商执照"""
    list_display = ["supplier","photo","name"]
    list_filter = ["supplier"]
    search_fields = ['supplier']
    model_icon = 'fa fa-cog'


class SupplierPhotoAdmin(object):
    """供应商照片"""
    list_display = ["supplier","photo","name"]
    list_filter = ["supplier"]
    search_fields = ['supplier']
    model_icon = 'fa fa-cog'


class SupplierContactAdmin(object):
    show_detail_fields = ['supplier']  # 在指定的字段后添加一个显示数据详情的一个按钮
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ['supplier', 'linkman', "category", "project", "description",  "receivable","receivable_remark",
                    "received", "received_remark","pending","pending_remark","date","delete_status"]
    list_filter = ['supplier', "category"]
    search_fields = ['project', ]
    ordering = ['-nid']
    model_icon = 'fa fa-cog'


class SupplierMemoAdmin(object):
    show_detail_fields = ['supplier']  # 在指定的字段后添加一个显示数据详情的一个按钮
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ['supplier', 'title','title',"detail"]
    list_filter = ['supplier', ]
    search_fields = ['supplier']
    ordering = ['-nid']
    model_icon = 'fa fa-cog'


class ContactAttachAdmin(object):
    """联系人附件"""
    list_display = ["contact","attachment","name", "description"]
    list_filter = ["contact"]
    search_fields = ['contact']
    model_icon = 'fa fa-cog'


class MemoAttachAdmin(object):
    """联系人附件"""
    list_display = ["memo","attachment","name", "description"]
    list_filter = ["memo"]
    search_fields = ['memo']
    model_icon = 'fa fa-cog'


class WastageGoodsAdmin(object):
    """损耗登记"""

    # def display_authors(self, obj=None, is_header=False):
    #     if is_header:
    #         return ""
    #     s = []
    #     for item in obj.solver.all():  # 必须使用all(),得到所有的处理对象
    #         s.append(item.name)  # 取出每个处理人的name属性
    #     val = " | ".join(s)
    #     return mark_safe(val)
    # display_authors.short_description = '处理人'

    def display_link(self, obj=None, is_header=False):
        if is_header:
            return ""
        eles = ""
        for item in obj.wastageattach_set.all():
            if item.attachment:
                eles += '<a class="download_file"  href="/attachment_download.html?url={0}&name={1}">{2}</a> <br>'.format(item.attachment,item.name,item.name)
        return format_html(eles)
    display_link.short_description = '附件'

    show_detail_fields = ['goods']  # 在指定的字段后添加一个显示数据详情的一个按钮
    # list_display_links_details = True  #:点击列表连接后是否转到详情页面
    fields = ('goods', 'unit','amount',"reason",'way','proposal',"date","solver","is_deleted")
    list_display = ['goods', 'unit','amount',"reason",'way','proposal',"solver","display_link","date"]
    list_filter = ['goods', ]
    search_fields = ['goods']
    ordering = ['-nid']
    # 后台自定义哪些字段只可读
    model_icon = 'fa fa-cog'

    # filter_horizontal = ('WastageSolver',)  # 关联表
    style_fields = {'solver': 'm2m_transfer'}


class WastageAttachAdmin(object):
    """损耗附件"""
    def display_link(self, obj=None, is_header=False):
        if is_header:
            return ""
        if obj.attachment:
            return format_html(
                '<a class="download_file"  href="/attachment_download.html?url={0}&name={1}">{2}</a>',
                obj.attachment,obj.name,obj.name)

    display_link.short_description = '附件链接'
    list_display = ["wastage","attachment","name","display_link", "description"]
    list_filter = ["wastage"]
    search_fields = ['wastage']
    model_icon = 'fa fa-cog'


# settings


#  admin models
xadmin.site.register(Supplier, SupplierAdmin)
xadmin.site.register(SupplierAttach, SupplierAttachAdmin)
xadmin.site.register(SupplierCategory, SupplierCategoryAdmin)
xadmin.site.register(SupplierLicence, SupplierLicenceAdmin)
xadmin.site.register(SupplierPhoto, SupplierPhotoAdmin)
xadmin.site.register(SupplierContact, SupplierContactAdmin)
xadmin.site.register(SupplierMemo, SupplierMemoAdmin)
xadmin.site.register(Goods, GoodsAdmin)
xadmin.site.register(GoodsAttach, GoodsAttachAdmin)
xadmin.site.register(GoodsCategory, GoodsCategoryAdmin)
xadmin.site.register(GoodsUnit, GoodsUnitAdmin)
xadmin.site.register(Industry, IndustryAdmin)
xadmin.site.register(Linkman, LinkmanAdmin)
xadmin.site.register(LinkmanAttach, LinkmanAttachAdmin)
xadmin.site.register(LinkmanPhoto, LinkmanPhotoAdmin)
xadmin.site.register(LinkmanCard, LinkmanCardAdmin)
xadmin.site.register(WastageGoods, WastageGoodsAdmin)
xadmin.site.register(WastageAttach, WastageAttachAdmin)








