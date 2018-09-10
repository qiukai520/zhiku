import xadmin
from xadmin import views
from .models import *


# admin models
class SupplierAdmin(object):
    """员工后台管理"""
    # list_display_links = ("job_number",)  #:显示修改或查看数据详情连接的列
    show_detail_fields = ['company']  # 在指定的字段后添加一个显示数据详情的一个按钮
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ['company','industry',"category","goods","phone","introduce","website","remark",]
    list_filter = ['industry',"category"]
    search_fields = ['company',]
    ordering = ['-nid']
    model_icon = 'fa fa-user'



class GoodsAdmin(object):
    """供应商品"""
    # list_display_links = ("job_number",)  #:显示修改或查看数据详情连接的列
    show_detail_fields = ['name']  # 在指定的字段后添加一个显示数据详情的一个按钮
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ['name', "category", "description", "unit", "standard", "start_time", "end_time", "country"]
    list_filter = ["category"]
    search_fields = ['name', ]
    ordering = ['-nid']
    model_icon = 'fa fa-user'


class LinkmanAdmin(object):
    """供应商联系人"""
    # list_display_links = ("job_number",)  #:显示修改或查看数据详情连接的列
    show_detail_fields = ['supplier']  # 在指定的字段后添加一个显示数据详情的一个按钮
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ['supplier','name',"gender","age","marriage","mobile","phone","birthday","native_place","delete_status"]
    list_filter = ['supplier',"gender"]
    search_fields = ['supplier', 'name',]
    ordering = ['-delete_status']
    model_icon = 'fa fa-user'


class GoodsAttachAdmin(object):
    """商品附件"""
    list_display = ["goods","attachment","name", "description"]
    list_filter = ["goods"]
    search_fields = ['goods']
    model_icon = 'fa fa-user'


class SupplierAttachAdmin(object):
    """供应商附件"""
    list_display = ["supplier","attachment","name", "description"]
    list_filter = ["supplier"]
    search_fields = ['supplier']
    model_icon = 'fa fa-user'


class LinkmanAttachAdmin(object):
    """联系人附件"""
    list_display = ["linkman","attachment","name", "description"]
    list_filter = ["linkman"]
    search_fields = ['supplier']
    model_icon = 'fa fa-user'


class SupplierLicenceAdmin(object):
    """供应商执照"""
    list_display = ["supplier","licence","name"]
    list_filter = ["supplier"]
    search_fields = ['supplier']
    model_icon = 'fa fa-user'


class SupplierPhotoAdmin(object):
    """供应商照片"""
    list_display = ["supplier","photo","name"]
    list_filter = ["supplier"]
    search_fields = ['supplier']
    model_icon = 'fa fa-user'


class GoodsUnitAdmin(object):
    """商品单位"""
    list_display = ["caption"]
    search_fields = ['caption']
    model_icon = 'fa fa-user'


class GoodsCategoryAdmin(object):
    """商品分类"""
    list_display = ["caption"]
    search_fields = ['caption']
    model_icon = 'fa fa-user'


class SupplierCategoryAdmin(object):
    """供应商分类"""
    list_display = ["caption"]
    search_fields = ['caption']
    model_icon = 'fa fa-user'


class IndustryAdmin(object):
    """行业"""
    list_display = ["industry"]
    search_fields = ['industry']
    model_icon = 'fa fa-user'


class NationAdmin(object):
    """国家"""
    list_display = ["nation"]
    search_fields = ['nation']
    model_icon = 'fa fa-user'


class ProvinceAdmin(object):
    """省份"""
    list_display = ["province","nation"]
    list_filter = ["nation"]
    search_fields = ['province']
    model_icon = 'fa fa-user'


class CityAdmin(object):
    """城市"""
    list_display = ["city","province"]
    list_filter = ["province"]
    search_fields = ['city']
    model_icon = 'fa fa-user'

class CountryAdmin(object):
    """县（区）"""
    list_display = ["country","city"]
    list_filter = ["city"]
    search_fields = ['country']
    model_icon = 'fa fa-user'

# settings


#  admin models
xadmin.site.register(Supplier, SupplierAdmin)
xadmin.site.register(SupplierAttach, SupplierAttachAdmin)
xadmin.site.register(SupplierCategory, SupplierCategoryAdmin)
xadmin.site.register(SupplierLicence, SupplierLicenceAdmin)
xadmin.site.register(SupplierPhoto, SupplierPhotoAdmin)
xadmin.site.register(Goods, GoodsAdmin)
xadmin.site.register(GoodsAttach, GoodsAttachAdmin)
xadmin.site.register(GoodsCategory, GoodsCategoryAdmin)
xadmin.site.register(GoodsUnit, GoodsUnitAdmin)
xadmin.site.register(Industry, IndustryAdmin)
xadmin.site.register(Linkman, LinkmanAdmin)
xadmin.site.register(LinkmanAttach, LinkmanAttachAdmin)
xadmin.site.register(Nation, NationAdmin)
xadmin.site.register(Province, ProvinceAdmin)
xadmin.site.register(City, CityAdmin)
xadmin.site.register(Country, CountryAdmin)




