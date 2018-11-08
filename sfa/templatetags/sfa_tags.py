
from django import template
from django.utils.safestring import mark_safe
from ..server import *
from personnel.server import *

register = template.Library()


@register.simple_tag
def build_customer_category_ele(selected=None):
    """构建客户分类下拉框"""
    print("category",selected)
    category_list = customer_category_db.query_category_list()
    eles = ""
    if selected:
        for item in category_list:
            if item.nid == selected:
                ele = """<option value={0} selected="selected" >{1}</option>""".format(item.nid, item.caption)
            else:
                ele = """<option value={0}>{1}</option>""".format(item.nid, item.caption)
            eles += ele
    else:
        for item in category_list:
            ele = """<option value={0}>{1}</option>""".format(item.nid, item.caption)
            eles += ele
    return mark_safe(eles)


@register.simple_tag
def build_follow_way_ele(selected=None):
    """构建跟进方式下拉框"""
    print("way", selected)
    way_list = follow_way_db.query_way_list()
    eles = ""
    if selected:
        for item in way_list:
            if item.nid == selected:
                ele = """<option value={0} selected="selected" >{1}</option>""".format(item.nid, item.content)
            else:
                ele = """<option value={0}>{1}</option>""".format(item.nid, item.content)
            eles += ele
    else:
        for item in way_list:
            ele = """<option value={0}>{1}</option>""".format(item.nid, item.content)
            eles += ele
    return mark_safe(eles)


@register.simple_tag
def build_follow_contact_ele(selected=None):
    """构建跟进联络方式下拉框"""
    contact_list = follow_contact_db.query_contact_list()
    eles = ""
    if selected:
        for item in contact_list:
            if item.nid == selected:
                ele = """<option value={0} selected="selected" >{1}</option>""".format(item.nid, item.content)
            else:
                ele = """<option value={0}>{1}</option>""".format(item.nid, item.content)
            eles += ele
    else:
        for item in contact_list:
            ele = """<option value={0}>{1}</option>""".format(item.nid, item.content)
            eles += ele
    return mark_safe(eles)


@register.simple_tag
def build_follow_linkman_ele(selected=None):
    """构建客户联系人下拉框"""
    linkman_list = follow_linkman_db.query_linkman_list()
    eles = ""
    if selected:
        for item in linkman_list:
            if item.nid == selected:
                ele = """<option value={0} selected="selected" >{1}</option>""".format(item.nid, item.content)
            else:
                ele = """<option value={0}>{1}</option>""".format(item.nid, item.content)
            eles += ele
    else:
        for item in linkman_list:
            ele = """<option value={0}>{1}</option>""".format(item.nid, item.content)
            eles += ele
    return mark_safe(eles)



@register.simple_tag
def build_follow_result_ele(selected=None):
    """构建客户需求意向下拉框"""
    result_list = follow_result_db.query_result_list()
    eles = ""
    if selected:
        for item in result_list:
            if item.nid == selected:
                ele = """<option value={0} selected="selected" >{1}</option>""".format(item.nid, item.content)
            else:
                ele = """<option value={0}>{1}</option>""".format(item.nid, item.content)
            eles += ele
    else:
        for item in result_list:
            ele = """<option value={0}>{1}</option>""".format(item.nid, item.content)
            eles += ele
    return mark_safe(eles)


@register.simple_tag
def build_customer_purpose_ele(selected=None):
    """构建客户意向下拉框"""
    purpose_list = customer_purpose_db.query_purpose_list()
    print("purpose_list",purpose_list)
    eles = ""
    if not selected:
        for item in purpose_list:
            if item.content == "D类":
                selected = item.nid  # 默认D类客户
    for item in purpose_list:
        if item.nid == selected:
            ele = """<option value={0} selected="selected" >{1}</option>""".format(item.nid, item.content)
        else:
            ele = """<option value={0}>{1}</option>""".format(item.nid, item.content)
        eles += ele
    return mark_safe(eles)


@register.simple_tag
def change_to_customer_purpose(id):
    if id:
        obj = customer_purpose_db.query_purpose_by_id(id)
        if obj:
            return obj.content

@register.simple_tag
def change_to_follow_way(id):
    if id:
        obj = follow_way_db.query_way_by_id(id)
        if obj:
            return obj.content
@register.simple_tag
def change_to_follow_contact(id):
    if id:
        obj = follow_contact_db.query_contact_by_id(id)
        if obj:
            return obj.content

@register.simple_tag
def change_to_follow_linkman(id):
    if id:
        obj = follow_linkman_db.query_linkman_by_id(id)
        if obj:
            return obj.content

@register.simple_tag
def change_to_follow_result(id):
    if id:
        obj = follow_result_db.query_result_by_id(id)
        if obj:
            return obj.content


@register.simple_tag
def change_to_customer_category(id):
    """转换成客户分类"""
    if id:
        obj = customer_category_db.query_category_by_id(id)
        if obj:
            return obj.caption

@register.simple_tag
def change_to_linkman(id):
    if id:
        obj = c_linkman_db.query_linkman_by_id(id)
        if obj:
            return obj.name


@register.simple_tag
def change_to_gender(id):
    gender_choice = c_linkman_db.gender_choice
    for item in gender_choice:
        if item['id'] == int(id):
            return item["caption"]

@register.simple_tag
def change_to_linkman_marriage(id):
    marriage_choice =c_linkman_db.marriage_choice
    for item in marriage_choice:
        if item['id'] == int(id):
            return item["caption"]


@register.simple_tag
def change_to_linkman_lunar(id):
    lunar_choice = c_linkman_db.lunar_choice
    for item in lunar_choice:
        if item['id'] == int(id):
            return item["caption"]


@register.simple_tag
def change_to_staff(id):
    if id:
        staff_obj = staff_db.query_staff_by_id(id)
        if staff_obj:
            return staff_obj.name

@register.simple_tag
def fetch_customer_linkman_list(id):
    if id :
        linkman_list = c_linkman_db.query_linkman_by_customer_id(id)
        return linkman_list


@register.simple_tag
def fetch_customer_memo_list(id):
    if id :
        memo_list = c_memo_db.query_memo_by_customer_id(id)
        return memo_list


@register.simple_tag
def fetch_customer_follow_list(id):
    if id:
        follow_list = c_follow_db.query_follow_by_customer_id(id)
        print("follow_list",follow_list)
        return follow_list