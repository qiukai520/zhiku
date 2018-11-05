
from django import template
from django.utils.safestring import mark_safe
from ..server import *

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
def build_customer_purpose_ele(selected=None):
    """构建客户分类下拉框"""
    purpose_list = customer_db.purpose_choice
    eles = ""
    if not selected:
        selected = 3  # 默认d类客户
    print("selected",selected)
    if selected:
        for item in purpose_list:
            if item.get("id") == selected:
                ele = """<option value={0} selected="selected" >{1}</option>""".format(item.get("id"),
                                                                                       item.get("caption"))
            else:
                ele = """<option value={0}>{1}</option>""".format(item.get("id"), item.get("caption"))
            eles += ele
    return mark_safe(eles)

@register.simple_tag
def change_to_customer_purpose(id):
    purpose_choice = customer_db.purpose_choice
    for item in purpose_choice:
        if item['id'] == int(id):
            return item["caption"]


@register.simple_tag
def change_to_customer_category(id):
    """转换成客户分类"""
    if id:
        obj = customer_category_db.query_category_by_id(id)
        if obj:
            return obj.caption

@register.simple_tag
def fetch_customer_linkman_list(id):
    if id :
        linkman_list = c_linkman_db.query_linkman_by_customer_id(id)
        return linkman_list


@register.simple_tag
def fetch_customer_memo_list(id):
    if id :
        linkman_list = c_memo_db.query_memo_by_customer_id(id)
        return linkman_list