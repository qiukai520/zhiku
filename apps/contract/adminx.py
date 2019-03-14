# -*- coding: utf-8 -*-
"""
@Author: Lee
@Date  : 2018/11/21 12:31
"""
import xadmin
from xadmin import views
from .models import *


class ContractInfoAdmin(object):
    """合同信息"""
    # list_display_links = ("",)  #:显示修改或查看数据详情连接的列
    show_detail_fields = ['identifier']  # 在指定的字段后添加一个显示数据详情的一个按钮
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ['identifier','customer',"product","product_meal","year_limit",'received',"sign","start_date"]
    list_filter = ['customer',"product","product_meal"]
    search_fields = ['customer',"product","product_meal"]
    ordering = ['sign']
    model_icon = 'fa fa-user'


class ContractAttachAdmin(object):
    """合同附件"""
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ['contract', 'attachment', "name", "description" ]
    ordering = ['-nid']
    model_icon = 'fa fa-cog'


class ProductMealAdmin(object):
    """产品套餐"""
    # list_display_links = ("code",)  #:显示修改或查看数据详情连接的列
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ["product","name","standard","price","year_limit"]
    list_filter = ["product"]
    search_fields = ["product" ]
    ordering = ['-nid']
    model_icon = 'fa fa-cog'


class ContractLocationAdmin(object):
    """合同存放位置"""
    # list_display_links = ("code",)  #:显示修改或查看数据详情连接的列
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ["location",]
    list_filter = ["location"]
    search_fields = ["location" ]
    ordering = ['-nid']
    model_icon = 'fa fa-cog'


class ProductAdmin(object):
    """产品"""
    # list_display_links = ("code",)  #:显示修改或查看数据详情连接的列
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ["name",]
    list_filter = ["name"]
    search_fields = ["name" ]
    ordering = ['-nid']
    model_icon = 'fa fa-cog'


class ApproverAdmin(object):
    """合同审批人"""
    # list_display_links = ("code",)  #:显示修改或查看数据详情连接的列
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ["Approver","follow"]
    list_filter = ["Approver",]
    search_fields = ["Approver" ,]
    ordering = ['-nid']
    model_icon = 'fa fa-cog'


class ApproverResultAdmin(object):
    """合同审核结果"""
    # list_display_links = ("code",)  #:显示修改或查看数据详情连接的列
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ["contract","approver","follow","result"]
    ordering = ['-nid']
    model_icon = 'fa fa-cog'


class ApproverRecordAdmin(object):
    """合同审核记录"""
    # list_display_links = ("code",)  #:显示修改或查看数据详情连接的列
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ["result","content","result2",]
    ordering = ['-nid']
    model_icon = 'fa fa-cog'


class ContractPaymentAdmin(object):
    """合同尾款"""
    # list_display_links = ("code",)  #:显示修改或查看数据详情连接的列
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ["contract","payment","date","remark"]
    ordering = ['-nid']
    model_icon = 'fa fa-cog'


class PaymentAttachAdmin(object):
    """尾款附件"""
    # list_display_links = ("code",)  #:显示修改或查看数据详情连接的列
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ["payment","attachment","name","description"]
    ordering = ['-nid']
    model_icon = 'fa fa-cog'


class PaymentApproveAdmin(object):
    """尾款审核结果"""
    # list_display_links = ("code",)  #:显示修改或查看数据详情连接的列
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ["payment","approver","follow","result"]
    ordering = ['-nid']
    model_icon = 'fa fa-cog'


class PaymentApproveRecordAdmin(object):
    """尾款审核记录"""
    # list_display_links = ("code",)  #:显示修改或查看数据详情连接的列
    # list_display_links_details = True  #: 点击列表连接后是否转到详情页面
    list_display = ["result","content","result2",]
    ordering = ['-nid']
    model_icon = 'fa fa-cog'


# settings

#  admin models
xadmin.site.register(ContractInfo, ContractInfoAdmin)
xadmin.site.register(ProductMeal, ProductMealAdmin)
xadmin.site.register(Product, ProductAdmin)
xadmin.site.register(Approver, ApproverAdmin)
xadmin.site.register(ApproverResult, ApproverResultAdmin)
xadmin.site.register(ContractPayment, ContractPaymentAdmin)
xadmin.site.register(ApproverRecord, ApproverRecordAdmin)
xadmin.site.register(PaymentAttach, PaymentAttachAdmin)
xadmin.site.register(PaymentApprove, PaymentApproveAdmin)
xadmin.site.register(PaymentApproveRecord, PaymentApproveRecordAdmin)




