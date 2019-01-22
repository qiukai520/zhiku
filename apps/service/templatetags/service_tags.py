from django import template
from django.utils.safestring import mark_safe
from ..server import *
register = template.Library()


@register.simple_tag
def build_crt_follow_way_ele(selected=None):
    """构建跟进方式下拉框"""
    way_list = way_db.query_way_list()
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
def build_crt_follow_contact_ele(selected=None):
    """构建跟进联络方式下拉框"""
    contact_list = contact_db.query_contact_list()
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
            ele = """<option value={0}>{1}</option>""".format(item.nid,item.content)
            eles += ele
    return mark_safe(eles)

