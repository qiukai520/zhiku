from django import template
from django.utils.safestring import mark_safe
from ..server import *

register = template.Library()

@register.simple_tag
def build_goods_category_ele(selected=None):
    """构建商品分类下拉框"""
    category_list = goods_category_db.query_category_list()
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
def build_goods_unit_ele(selected=None):
    """构建商品分类下拉框"""
    unit_list = goods_unit_db.query_unit_list()
    eles = ""
    if selected:
        for item in unit_list:
            if item.nid == selected:
                ele = """<option value={0} selected="selected" >{1}</option>""".format(item.nid, item.caption)
            else:
                ele = """<option value={0}>{1}</option>""".format(item.nid, item.caption)
            eles += ele
    else:
        for item in unit_list:
            ele = """<option value={0}>{1}</option>""".format(item.nid, item.caption)
            eles += ele
    return mark_safe(eles)


@register.simple_tag
def build_supplier_category_ele(selected=None):
    """构建供应商分类下拉框"""
    category_list = supplier_category_db.query_category_list()
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
def build_industry_category_ele(selected=None):
    """构建供应商行业下拉框"""
    industry_list = industry_db.query_industry_list()
    eles = ""
    if selected:
        for item in industry_list:
            if item.nid == selected:
                ele = """<option value={0} selected="selected" >{1}</option>""".format(item.nid, item.industry)
            else:
                ele = """<option value={0}>{1}</option>""".format(item.nid, item.industry)
            eles += ele
    else:
        for item in industry_list:
            ele = """<option value={0}>{1}</option>""".format(item.nid, item.industry)
            eles += ele
    return mark_safe(eles)



@register.simple_tag
def build_goods_ele(selected=None):
    """构建商品下拉框"""
    goods_list = goods_db.query_goods_list()
    eles = ""
    if selected:
        for item in goods_list:
            if item.nid == selected:
                ele = """<option value={0} selected="selected" >{1}</option>""".format(item.nid, item.name)
            else:
                ele = """<option value={0}>{1}</option>""".format(item.nid, item.name)
            eles += ele
    else:
        for item in goods_list:
            ele = """<option value={0}>{1}</option>""".format(item.nid, item.name)
            eles += ele
    return mark_safe(eles)


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
def build_city_ele(province_id=None, city_id=None):
    """构建城市下拉框"""
    if province_id:
        city_list = city_db.query_city_by_province(province_id)
    else:
        city_list = city_db.query_city_list()
    eles = ""
    if city_id:
        for item in city_list:
            if item.nid == city_id:
                ele = """<option selected=selected value={0}>{1}</option>""".format(item.nid, item.city)
            else:
                ele = """<option value={0}>{1}</option>""".format(item.nid, item.city)
            eles += ele
    else:
        for item in city_list:
            ele = """<option value={0}>{1}</option>""".format(item.nid, item.city)
            eles += ele
    return mark_safe(eles)


@register.simple_tag
def build_country_ele(city_id=None, selected=None):
    """构建城市下拉框"""
    if city_id:
        country_list = country_db.query_country_by_city(city_id)
    else:
        country_list = country_db.query_country_list()
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
def change_to_goods_category(id):
    """转换成商品分类"""
    if id:
        obj = goods_category_db.query_category_by_id(id)
        if obj:
            return obj.caption


@register.simple_tag
def change_to_supplier_category(id):
    """转换成供应商分类"""
    if id:
        obj = supplier_category_db.query_category_by_id(id)
        if obj:
            return obj.caption

@register.simple_tag
def change_to_industry(id):
    """转换行业分类"""
    if id:
        obj = industry_db.query_industry_by_id(id)
        if obj:
            return obj.industry


@register.simple_tag
def change_to_goods(id):
    """转换成商品"""
    if id:
        obj = goods_db.query_goods_by_id(id)
        if obj:
            return obj.name


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
    """根据城市获取省份nid"""
    if country_id:
        obj = country_db.query_country_by_id(country_id)
        if obj:
            return obj.city_id

@register.simple_tag
def fetch_goods_photo(id):
    """获取商品图片"""

    if id:
        obj = goods_photo_db.query_goods_photo(id)
        if obj:
            return obj.photo