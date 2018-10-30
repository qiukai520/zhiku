from django import template
from django.utils.safestring import mark_safe
from ..server import *
from personnel.server import staff_db

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
def build_warehouse_ele(selected=None):
    """构建商品分类下拉框"""
    warehouse_list = warehouse_db.query_warehouse_list()
    eles = ""
    if selected:
        for item in warehouse_list:
            if item.nid == selected:
                ele = """<option value={0} selected="selected" >{1}</option>""".format(item.nid, item.name)
            else:
                ele = """<option value={0}>{1}</option>""".format(item.nid, item.name)
            eles += ele
    else:
        for item in warehouse_list:
            ele = """<option value={0}>{1}</option>""".format(item.nid, item.name)
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
def build_supplier_ele(selected=None):
    """构建供应商下拉框"""
    supplier_list = supplier_db.query_supplier_list()
    eles = ""
    if selected:
        for item in supplier_list:
            if item.nid == selected:
                ele = """<option value={0} selected="selected" >{1}</option>""".format(item.nid, item.company)
            else:
                ele = """<option value={0}>{1}</option>""".format(item.nid, item.company)
            eles += ele
    else:
        for item in supplier_list:
            ele = """<option value={0}>{1}</option>""".format(item.nid, item.company)
            eles += ele
    return mark_safe(eles)


@register.simple_tag
def build_retailer_ele(selected=None):
    """构建零售商下拉框"""
    retailer_list = retailer_db.query_retail_list()
    eles = ""
    if selected:
        for item in retailer_list:
            if item.nid == selected:
                ele = """<option value={0} selected="selected" >{1}</option>""".format(item.nid, item.caption)
            else:
                ele = """<option value={0}>{1}</option>""".format(item.nid, item.caption)
            eles += ele
    else:
        for item in retailer_list:
            ele = """<option value={0}>{1}</option>""".format(item.nid, item.caption)
            eles += ele
    return mark_safe(eles)


@register.simple_tag
def build_contact_category_ele(selected=None):
    """构建交易分类下拉框"""
    category_list = supplier_contact_db.category
    eles = ""
    if selected:
        for item in category_list:
            if item['id'] == selected:
                ele = """<option value={0} selected="selected" >{1}</option>""".format(item['id'], item['caption'])
            else:
                ele = """<option value={0}>{1}</option>""".format(item['id'], item['caption'])
            eles += ele
    else:
        for item in category_list:
            ele = """<option value={0}>{1}</option>""".format(item['id'], item['caption'])
            eles += ele
    return mark_safe(eles)


@register.simple_tag
def build_supplier_linkman_ele(supplier_id,selected=None):
    print("supplier_id",supplier_id)
    linkman_list = linkman_db.query_linkman_by_supplier_id(supplier_id)
    eles = ""
    if selected:
        for item in linkman_list:
            if item.nid == selected:
                ele = """<option value={0} selected="selected" >{1}</option>""".format(item.nid, item.name)
            else:
                ele = """<option value={0}>{1}</option>""".format(item.nid, item.name)
            eles += ele
    else:
        for item in linkman_list:
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
def change_to_warehouse(id):
    """根据id转换成仓库"""
    if id:
        obj = warehouse_db.query_warehouse_by_id(id)
        if obj:
            return obj.name


@register.simple_tag
def change_to_warelocation(id):
    """根据id转换成库位"""
    if id:
        obj = ware_location_db.query_location_by_id(id)
        if obj:
            return obj.location


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
def change_to_contact_category(id):
    category_list = supplier_contact_db.category
    for item in category_list:
        print("item",item)
        if item['id'] == int(id):
            return item["caption"]

@register.simple_tag
def change_to_linkman(id):
    if id:
        obj = linkman_db.query_linkman_by_id(id)
        if obj:
            return obj.name


@register.simple_tag
def change_to_gender(id):
    gender_choice = linkman_db.gender_choice
    for item in gender_choice:
        print("item", item)
        if item['id'] == int(id):
            return item["caption"]

@register.simple_tag
def change_to_linkman_marriage(id):
    marriage_choice = linkman_db.marriage_choice
    for item in marriage_choice:
        print("item", item)
        if item['id'] == int(id):
            return item["caption"]


@register.simple_tag
def change_to_linkman_lunar(id):
    lunar_choice = linkman_db.lunar_choice
    for item in lunar_choice:
        print("item", item)
        if item['id'] == int(id):
            return item["caption"]

@register.simple_tag
def change_to_goods_category(id):
    """转换成商品分类"""
    if id:
        obj = goods_category_db.query_category_by_id(id)
        if obj:
            return obj.caption
@register.simple_tag
def change_to_goods_unit(id):
    """转换成商品单位"""
    if id:
        unit_obj=goods_unit_db.query_unit_by_id(id)
        if unit_obj:
            return unit_obj.caption


@register.simple_tag
def change_to_supplier(id):
    """转换成供应商分类"""
    if id:
        obj = supplier_db.query_supplier_by_id(id)
        if obj:
            return obj.company

@register.simple_tag
def change_to_retailer(id):
    """转换成比价供应商"""
    if id:
        obj = retailer_db.query_retail_by_id(id)
        if obj:
            return obj.caption



@register.simple_tag
def change_to_staff(id):
    if id:
        staff_obj = staff_db.query_staff_by_id(id)
        print("staff",staff_obj)
        if staff_obj:
            return staff_obj.name


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
def fetch_goods_photo(photo_str):
    """获取商品第一张图片"""
    import json
    if photo_str:
        photo_list = json.loads(photo_str)
        if len(photo_list):
            path = photo_list[0]
        else:
            path= ""
    else:
        path = ""
    return path


@register.simple_tag
def fetch_goods_total_amount(gid):
    """获取商品库存总数"""
    if gid:
        total_obj = invent_db.query_goods_total_amount(gid)
        total_amount = total_obj[0]
        if not total_amount:
            total_amount = 0
        return total_amount


@register.simple_tag
def fetch_warehouse_list():
    ware_list = warehouse_db.query_warehouse_list()
    return ware_list

@register.simple_tag
def fetch_goods_total_amount_by_warehouse(gid,wid):
    total_obj = invent_db.query_goods_total_amount_by_warehouse(gid,wid)
    total_amount = total_obj[0]
    if not total_amount:
        total_amount = 0
    return total_amount

@register.simple_tag
def fetch_location_by_goods_last(gid):
    invent_obj = invent_db.query_invent_by_goods(gid)
    location = "空"
    if invent_obj:
        location_id = invent_obj.location_id
        if location_id:
            location_obj = ware_location_db.query_location_by_id(location_id)
            if location_obj:
                location = location_obj.location
    return location

@register.simple_tag
def build_warelocation_ele(house_id,selected=None):
    """构建库位下拉框"""
    location_list = ware_location_db.query_location_by_house(house_id)
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
def fetch_invent_by_goods(gid):
    if gid:
        invent_record = invent_db.query_invent_by_goods_list(gid)
        return invent_record


@register.simple_tag
def fetch_purchase(pid):
    if pid:
        purchase_record = purchase_db.query_purchase_by_id(pid)
        return purchase_record



@register.simple_tag
def fetch_purchase_by_goods(gid):
    if gid:
        purchase_record = purchase_db.query_purchase_by_goods_list(gid)
        return purchase_record

@register.simple_tag
def fetch_supplier_linkman_list(id):
    if id :
        linkman_list = linkman_db.query_linkman_by_supplier_id(id)
        return linkman_list

@register.simple_tag
def fetch_supplier_contact_list(id):
    if id:
        contact_list = supplier_contact_db.query_contact_by_supplier(id)
        return contact_list

@register.simple_tag
def fetch_supplier_memo_list(id):
    if id:
        memo_list = supplier_memo_db.query_memo_by_supplier_id(id)
        return memo_list

@register.simple_tag
def fetch_goods_price_list(id):
    if id:
        goods_list = goods_price_db.query_price_by_goods(id)
        return goods_list

@register.simple_tag
def fetch_compare_price_list(id):
    if id:
        compare_list = price_compare_db.query_price_by_goods(id)
        return compare_list


@register.simple_tag
def fetch_warehouse(house_id):
    """根据县获取城市nid"""
    if house_id:
        obj = warehouse_db.query_warehouse_by_id(house_id)
        if obj:
            return obj



@register.simple_tag
def load_json(json_obj):
    """解析json对象"""
    import json
    if json_obj:
        data = json.loads(json_obj)
    else:
        data = []
    return data
