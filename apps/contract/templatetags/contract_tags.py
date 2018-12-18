from django import template
from django.utils.safestring import mark_safe
from ..server import *
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
def change_to_product(product_id):
    """产品"""
    if product_id:
        product_obj = product_db.query_product_by_id(product_id)
        if product_obj:
            return product_obj.name
        return "空"