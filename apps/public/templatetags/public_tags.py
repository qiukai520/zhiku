
from django import template
from django.utils.safestring import mark_safe
from ..server import *


register = template.Library()


@register.simple_tag
def build_nation_ele(selected=None):
    """构建国家下拉框"""
    nation_list = nation_db.query_nation_list()
    eles = ""
    if selected:
        for item in nation_list:
            if item.nid == selected:
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
    if nation_id:
        province_list = province_db.query_province_by_nation(nation_id)
    else:
        province_list = province_db.query_province_list()
    eles = ""
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
def build_province_ele(province_id=None):
    province_list = province_db.query_province_list()
    eles = ""
    if not province_id:
        province_id = 19 # 默认广东
    for item in province_list:
        if item.nid == province_id:
            ele = """<option selected=selected value={0}>{1}</option>""".format(item.nid, item.province)
        else:
            ele = """<option value={0}>{1}</option>""".format(item.nid, item.province)
        eles += ele
    return mark_safe(eles)

@register.simple_tag
def build_city_ele(province_id=None, city_id=None):
    """构建城市下拉框"""
    if not province_id:
       province_id = 19 # 默认广东
    city_list = city_db.query_city_by_province(province_id)
    eles = ""
    if not city_id:
        city_id = 197 #默认广州
    for item in city_list:
        if item.nid == city_id:
            ele = """<option selected=selected value={0}>{1}</option>""".format(item.nid, item.city)
        else:
            ele = """<option value={0}>{1}</option>""".format(item.nid, item.city)
        eles += ele
    return mark_safe(eles)


@register.simple_tag
def build_country_ele(city_id=None, selected=None):
    """构建县区下拉框"""
    if city_id:
        country_list = country_db.query_country_by_city(city_id)
    else:
        city_id = 197 # 默认广州
        country_list = country_db.query_country_by_city(city_id)
    eles = ""
    if selected:
        for item in country_list:
            if item.nid==selected:
                ele = """<option selected=selected value={0}>{1}</option>""".format(item.nid, item.country)
            else:
                ele = """<option value={0}>{1}</option>""".format(item.nid, item.country)
            eles += ele
    else:
        for item in country_list:
            ele = """<option value={0}>{1}</option>""".format(item.nid, item.country)
            eles += ele
    return mark_safe(eles)


@register.simple_tag
def build_town_ele(country_id=None, selected=None):
    """构建城市下拉框"""
    if country_id:
        town_list = town_db.query_town_by_country(country_id)
    else:
        town_list = town_db.query_town_list()
    eles = ""
    if selected:
        for item in town_list:
            if item.nid == selected:
                ele = """<option selected=selected value={0}>{1}</option>""".format(item.nid, item.town)
            else:
                ele = """<option value={0}>{1}</option>""".format(item.nid, item.town)
            eles += ele
    else:
        for item in town_list:
            ele = """<option value={0}>{1}</option>""".format(item.nid, item.town)
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
    if id:
        obj = province_db.query_province_by_id(id)
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
def change_to_country(id):
    """根据id转换成县区"""
    if id:
        obj = country_db.query_country_by_id(id)
        if obj:
            return obj.country
@register.simple_tag

def change_to_town(id):
    """根据id转换成街道"""
    if id:
        obj = town_db.query_town_by_id(id)
        if obj:
            return obj.town
@register.simple_tag
def fetch_nation_nid(province_id):
    """根据省份获取国家nid"""
    if province_id:
        obj = province_db.query_province_by_id(province_id)
        if obj:
            return obj.nation_id

@register.simple_tag
def fetch_province_nid(city_id):
    """根据城市获取省份nid"""
    if city_id:
        obj = city_db.query_city_by_id(city_id)
        if obj:
            return obj.province_id

@register.simple_tag
def fetch_city_nid(country_id):
    """根据县获取城市nid"""
    if country_id:
        obj = country_db.query_country_by_id(country_id)
        if obj:
            return obj.city_id

@register.simple_tag
def fetch_country_nid(town_id):
    """根据街道获取县id"""
    if town_id:
        obj = town_db.query_town_by_id(town_id)
        if obj:
            return obj.country_id


@register.simple_tag
def custom_mod(dividend,divisor):
    """取余"""
    mod = int(dividend) % int(divisor)
    return mod