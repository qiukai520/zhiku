from django import template
from django.utils.safestring import mark_safe
from ..server import *
from sfa.server import customer_db
from personnel.server import staff_db
register = template.Library()



@register.simple_tag
def build_product_ele(selected=None):
    """构建产品下拉框"""
    product_list = product_db.query_product_list()
    eles = ""
    if selected:
        for item in product_list:
            if item.nid == selected:
                ele = """<option value={0} selected="selected" >{1}</option>""".format(item.nid, item.name)
            else:
                ele = """<option value={0}>{1}</option>""".format(item.nid, item.name)
            eles += ele
    else:
        for item in product_list:
            ele = """<option value={0}>{1}</option>""".format(item.nid, item.name)
            eles += ele
    return mark_safe(eles)


@register.simple_tag
def build_location_ele(selected=None):
    """合同存档坐标下拉框"""
    location_list = c_location_db.query_location_list()
    eles = ""
    if selected:
        for item in location_list:
            if item.nid == selected:
                ele = """<option value={0} selected="selected" >{1}</option>""".format(item.nid, item.location)
            else:
                ele = """<option value={0}>{1}</option>""".format(item.nid, item.location)
            eles += ele
    else:
        for item in location_list:
            ele = """<option value={0}>{1}</option>""".format(item.nid, item.location)
            eles += ele
    return mark_safe(eles)

@register.simple_tag
def build_product_meal_ele(product=None, selected=None):
    """构建产品套餐下拉框"""
    meal_list = product_meal_db.query_meal_list()
    if product:
        meal_list.filter(product_id=product).all()
    eles = ""
    if selected:
        for item in meal_list:
            if item.nid == selected:
                ele = """<option value={0} selected="selected" >{1}</option>""".format(item.nid, item.name)
            else:
                ele = """<option value={0}>{1}</option>""".format(item.nid, item.name)
            eles += ele
    else:
        for item in meal_list:
            ele = """<option value={0}>{1}</option>""".format(item.nid, item.name)
            eles += ele
    return mark_safe(eles)


@register.simple_tag
def change_to_product(product_id):
    """产品"""
    if product_id:
        product_obj = product_db.query_product_by_id(product_id)
        if product_obj:
            return product_obj.name
        return "空"

@register.simple_tag
def change_to_location(location_id):
    """存档坐标"""
    if location_id:
        location_obj = c_location_db.query_location_by_id(location_id)
        if location_obj:
            return location_obj.location
    return "空"

@register.simple_tag
def change_to_product_meal(meal_id):
    """产品"""
    if meal_id:
        meal_obj = product_meal_db.query_meal_by_id(meal_id)
        if meal_obj:
            return meal_obj.name + "(" + str(meal_obj.price) + ")"
        return "空"


@register.simple_tag
def change_to_customer(customer_id):
    """客户"""
    if customer_id:
        customer_obj = customer_db.query_customer_by_id(customer_id)
        if customer_obj:
            return customer_obj.company
        return "空"

@register.simple_tag
def change_to_staff(sid):
    """员工"""
    if sid:
        staff_obj = staff_db.query_staff_by_id(sid)
        if staff_obj:
            return staff_obj.name
        return "空"


@register.simple_tag
def count_unapproved_paymemnt(cid,user):
    if cid and user:
        payment_list = payment_db.query_payment_by_contract(cid)
        count = 0
        for item in payment_list:
            num = p_apr_db.count_unapprove(item.nid,user)
            count += num
        return count
    return 0

@register.simple_tag
def fetch_my_approved_result(cid,sid):
    """获取我的审核结果"""
    if cid and sid:
        result_obj = approver_result_db.query_my_approved_result(cid,sid)
        if result_obj:
            return result_obj.result


@register.simple_tag
def fetch_my_approved_record(cid,user):
    if cid and user:
        result_obj = approver_result_db.query_my_approved_result(cid, user)
        if result_obj:
            record_list = app_record_db.query_my_record(result_obj.nid)
            if record_list:
                return record_list
    return []


@register.simple_tag
def fetch_my_approved_follow(cid,sid):
    """查看是否可以审核合同"""
    # 获取所有审核人
    flag = True
    appr_list = approver_result_db.query_record_by_contract(cid)
    if appr_list:
        if appr_list.first().follow > 0:
        # 有序审核
            for item in appr_list:
                if item.approver_id == sid:
                    my_follow = item.follow
                else:
                    my_follow = 0
            for item in appr_list:
                if item.follow < my_follow:
                    if item.result != 1:
                        flag = False
    return flag

@register.simple_tag
def fetch_approved_record_list(cid):
    """获取合同审核记录"""
    if cid:
        appr_list = approver_result_db.query_record_by_contract(cid)
        return appr_list


@register.simple_tag
def fetch_my_payment_approved_result(pid,sid):
    """获取我的尾款审核结果"""
    print("pid&sid",pid,sid)
    if pid and sid:
        result_obj = p_apr_db.query_my_approved_result(pid,sid)
        if result_obj:
            print("result_obj",result_obj.result)
            return result_obj.result


@register.simple_tag
def fetch_my_payment_approved_follow(pid,sid):
    """查看是否可以审核尾款"""
    # 获取所有审核人
    flag = True
    appr_list = p_apr_db.query_result_by_payment(pid)
    if appr_list:
        if appr_list.first().follow > 0:
        # 有序审核
            for item in appr_list:
                if item.approver_id == sid:
                    my_follow = item.follow
                else:
                    my_follow=0
            for item in appr_list:
                if item.follow < my_follow:
                    if item.result != 1:
                        flag = False
    return flag




@register.simple_tag
def fetch_payment_list(cid):
    if cid:
        payment_list = payment_db.query_payment_by_contract(cid)
        return payment_list


@register.simple_tag
def fetch_payment_approve_record(rid):
    if rid:
        record_list = p_apr_rcd_db.query_my_record(rid)
    else:
        record_list = []
    return record_list


@register.simple_tag
def fetch_contract_approve_record(rid):
    print("rid",rid)
    if rid:
        record_list = app_record_db.query_my_record(rid)
    else:
        record_list = []
    return record_list