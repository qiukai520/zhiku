from django import template
from django.utils.safestring import mark_safe
from ..server import *



register = template.Library()

@register.simple_tag
def build_nation_ele(select=None):
    """构建国家下拉框"""
    nation_list = nation_db.query_nation_list()
    eles = ""
    if select:
        for item in nation_list:
            if item.nid == select:
                ele = """<option value={0} selected="selected" >{1}</option>""".format(item.nid, item.nation)
            else:
                ele = """<option value={0}>{1}</option>""".format(item.nid, item.nation)
            eles += ele
    else:
        for item in nation_list:
            ele = """<option value={0}>{1}</option>""".format(item.nid, item.nation)
            eles += ele
    return mark_safe(eles)

@register.simple_tag
def build_province_ele(nation_id=None,province_id=None):
    """构建省份下拉框"""
    print("nation_id",nation_id)
    if nation_id:
        province_list = province_db.query_province_by_nation(nation_id)
    else:
        province_list = province_db.query_province_list()
    eles = ""
    print("province_list",province_list)
    if province_id:
        for item in province_list:
            if item.nid == province_id:
                ele = """<option selected=selected value={0}>{1}</option>""".format(item.nid, item.province)
            else:
                ele = """<option value={0}>{1}</option>""".format(item.nid, item.province)
            eles += ele
    else:
        for item in province_list:
            ele = """<option value={0}>{1}</option>""".format(item.nid, item.province)
            eles += ele
    return mark_safe(eles)


@register.simple_tag
def build_city_ele(province_id=None):
    """构建城市下拉框"""
    if province_id:
        city_list = city_db.query_city_by_province(province_id)
    else:
        city_list = city_db.query_city_list()
    eles = ""
    for item in city_list:
        ele = """<option value={0}>{1}</option>""".format(item.nid, item.city)
        eles += ele
    return mark_safe(eles)


@register.simple_tag
def change_to_nation(id):
    """根据id转换成国家"""
    if id:
        obj = nation_db.query_nation_by_id(id)
        if obj:
            return obj.nation


@register.simple_tag
def change_to_province(id):
    """根据id转换成省份"""
    print("province",id)
    if id:
        obj = province_db.query_province_by_id(id)
        print(obj)
        if obj:

            return obj.province


@register.simple_tag
def change_to_city(id):
    """根据id转换成城市"""
    if id:
        obj = city_db.query_city_by_id(id)
        if obj:
            return obj.city


@register.simple_tag
def fetch_nation_nid(province_id):
    """根据省份获取国家nid"""
    print("province_id",province_id)
    if province_id:
        obj = province_db.query_province_by_id(province_id)
        return obj.nation_id


@register.simple_tag
def fetch_province_nid(city_id):
    """根据城市获取省份nid"""
    if city_id:
        obj = city_db.query_city_by_id(city_id)
        print("obj.province_id",obj.province_id)
        return obj.province_id