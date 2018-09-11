from django import template
from django.utils.safestring import mark_safe
from ..server import *



register = template.Library()

@register.simple_tag
def build_nation_ele():
    """构建国家下拉框"""
    nation_list = nation_db.query_nation_list()
    eles = ""
    for item in nation_list:
        ele = """<option value={0}>{1}</option>""".format(item.nid, item.nation)
        eles += ele
    return mark_safe(eles)


@register.simple_tag
def change_to_nation(id):
    """根据id转换成国家"""
    if id:
        obj = nation_db.query_nation_by_id(id)
        if obj:
            return obj.nation


