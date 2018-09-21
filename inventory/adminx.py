import xadmin
from xadmin import views
from .models import *


# admin models


class GoodsUnitAdmin(object):
    """商品单位"""
    list_display = ["caption"]
    search_fields = ['caption']
    model_icon = 'fa fa-cog'

class GoodsCategoryAdmin(object):
    """商品分类"""
    list_display = ["caption"]
    search_fields = ['caption']
    model_icon = 'fa fa-cog'

class GoodsAdmin(object):
    """供应商品"""
    # list_display_links = ("job_number",)  #:显示修改或查看数据详情连接的列
    show_detail_fields = ['name']  # 在指定的字段后添加一个显示数据详情的一个按钮
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ['name', "category", "description", "unit", "standard","start_month", "end_month", "country"]
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
    list_display = ['company','industry',"category","goods","phone","introduce","website","remark",]
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
    list_display = ["supplier","licence","name"]
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
# 地区
# 地区


class NationAdmin(object):
    """国家"""
    list_display = ["nation"]
    search_fields = ['nation']
    model_icon = 'fa fa-cog'


class ProvinceAdmin(object):
    """省份"""
    list_display = ["province","nation"]
    list_filter = ["nation"]
    search_fields = ['province']
    model_icon = 'fa fa-cog'


class CityAdmin(object):
    """城市"""
    list_display = ["city","province"]
    list_filter = ["province"]
    search_fields = ['city']
    model_icon = 'fa fa-cog'


class CountryAdmin(object):
    """县（区）"""
    list_display = ["country","city"]
    list_filter = ["city"]
    search_fields = ['country']
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
xadmin.site.register(Nation, NationAdmin)
xadmin.site.register(Province, ProvinceAdmin)
xadmin.site.register(City, CityAdmin)
xadmin.site.register(Country, CountryAdmin)




