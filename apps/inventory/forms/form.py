from .validate_func import *
from django.forms import fields as django_fields
from django.forms import forms as django_forms


class IndustryForm(django_forms.Form):
    industry = django_fields.CharField(error_messages={"required": "行业名称不能为空"})


class SupplierCategoryForm(django_forms.Form):
    caption = django_fields.CharField(error_messages={"required": "供应商分类名称不能为空"})


class RetailSupplierForm(django_forms.Form):
    caption = django_fields.CharField(error_messages={"required": "零售供应商不能为空"})


class GoodsCategoryForm(django_forms.Form):
    caption = django_fields.CharField(error_messages={"required": "商品分类名称不能为空"})


class GoodsUnitForm(django_forms.Form):
    caption = django_fields.CharField(error_messages={"required": "商品单位名称不能为空"})


class JobTitlekForm(django_forms.Form):
    job_title = django_fields.CharField(error_messages={"required": "职称不能为空"})


class GoodsForm(django_forms.Form):
    category_id = django_fields.IntegerField(error_messages={"required": "请选择商品分类",})
    name = django_fields.CharField(error_messages={"required":"商品名称不能为空"})

class SupplierForm(django_forms.Form):
    category_id = django_fields.IntegerField(error_messages={"required": "请选择商品分类"})
    company = django_fields.CharField(error_messages={"required": "公司名称不能为空"})
    town_id = django_fields.IntegerField(min_value=1 , error_messages={"required": "请选择街道","min_value":"请选择街道"})
    products = django_fields.CharField(error_messages={"required": "主营商品不能为空"})


class LinkmanForm(django_forms.Form):
    supplier_id = django_fields.IntegerField(error_messages={"required": "请选择供应商"})
    name = django_fields.CharField(error_messages={"required": "联系人姓名不能为空"})
    birthday = django_fields.DateField(error_messages={"required": "生日不能为空", "invalid": "生日日期格式错误"})


class ContactForm(django_forms.Form):
    supplier_id = django_fields.IntegerField(error_messages={"required": "请选择供应商"})
    category = django_fields.IntegerField(error_messages={"required": "请选择交易分类"})
    linkman_id = django_fields.IntegerField(error_messages={"required": "请选择联系人"})
    project = django_fields.CharField(error_messages={"required": "交易项目不能为空"})
    date = django_fields.DateField(error_messages={"required": "交易日期不能为空", "invalid": "日期格式错误"})


class MemoForm(django_forms.Form):
    supplier_id = django_fields.IntegerField(error_messages={"required": "请选择供应商"})
    title = django_fields.CharField(error_messages={"required": "标题不能为空"})
    detail = django_fields.CharField(error_messages={"required": "详细不能为空"})


class PriceForm(django_forms.Form):
    supplier_id = django_fields.IntegerField(min_value=1, error_messages={"required": "请选择供应商","min_value":"请选择供应商"})
    linkman_id = django_fields.IntegerField(min_value=1,error_messages={"required": "请选择联系人","min_value":"请选择联系人"})
    amount = django_fields.IntegerField(error_messages={"required": "请输入数量","invalid": "请输入合法的数字"})
    price = django_fields.DecimalField(max_digits=8, decimal_places=2,error_messages={"required": "请输入价格",
                                                                                            "invalid": "请输入合法的价格"})
    date = django_fields.DateField(error_messages={"required": "报价日期不能为空", "invalid": "日期格式错误"})
    logistics = django_fields.DecimalField(max_digits=8, decimal_places=2,error_messages={"required": "请输入价格", "invalid": "请输入合法的价格"})


class PriceCompareForm(django_forms.Form):
    retail_id = django_fields.IntegerField(min_value=1, error_messages={"required": "请选择零售商","min_value":"请选择零售商"})
    amount = django_fields.IntegerField(error_messages={"required": "请输入数量","invalid": "请输入合法的数字"})
    price = django_fields.DecimalField(max_digits=8, decimal_places=2,error_messages={"required": "请输入价格",
                                                                                            "invalid": "请输入合法的价格"})
    date = django_fields.DateField(error_messages={"required": "比价日期不能为空", "invalid": "日期格式错误"})


class NationForm(django_forms.Form):
    nation = django_fields.CharField(error_messages={"required": "国家名称不能为空"})


class ProvinceForm(django_forms.Form):
    province = django_fields.CharField(error_messages={"required": "省份不能为空"})
    nation_id = django_fields.IntegerField(error_messages={"required":"请选择国家"})


class CityForm(django_forms.Form):
    city = django_fields.CharField(error_messages={"required": "城市不能为空"})
    province_id = django_fields.IntegerField(error_messages={"required":"请选择省份"})


class CountryForm(django_forms.Form):
    country = django_fields.CharField(error_messages={"required": "县区不能为空"})
    city_id = django_fields.IntegerField(error_messages={"required": "请选择城市"})


class TownForm(django_forms.Form):
    town = django_fields.CharField(error_messages={"required": "镇不能为空"})
    country_id = django_fields.IntegerField(error_messages={"required": "请选择县(区)","invalid": "请输入合法的县(区)"})


class WarehouseForm(django_forms.Form):
    name = django_fields.CharField(error_messages={"required": "仓库名称不能为空"})
    town_id = django_fields.IntegerField(min_value=1 , error_messages={"required": "请选择街道","min_value":"请选择街道"})
    address = django_fields.CharField(error_messages={"required": "地址不能为空"})


class WareLocationForm(django_forms.Form):
    location = django_fields.CharField(error_messages={"required": "库位名称不能为空"})
    warehouse_id = django_fields.IntegerField(error_messages={"required":"请选择仓库"})


class InventForm(django_forms.Form):
    goods_id = django_fields.IntegerField(error_messages={"required":"商品不能为空"})
    warehouse_id = django_fields.IntegerField(error_messages={"required":"仓库不能为空"})
    location_id = django_fields.CharField(error_messages={"required":"库位不能为空"})
    amount = django_fields.IntegerField(error_messages={"required":"数量不能为空"})
    date = django_fields.DateField(error_messages={"required":"入库日期不能为空"})
    unit_id=django_fields.IntegerField(error_messages={"required":"单位不能为空  "})


class PurchaseForm(django_forms.Form):
    goods_id = django_fields.IntegerField(error_messages={"required": "采购商品不能为空"})
    supplier_id = django_fields.IntegerField(error_messages={"required": "供应商不能为空"})
    linkman_id = django_fields.CharField(error_messages={"required": "联系人不能为空"})
    amount = django_fields.IntegerField(error_messages={"required": "数量不能为空"})
    date = django_fields.DateField(error_messages={"required": "采购日期不能为空", "invalid": "日期格式错误"})
    unit_id = django_fields.IntegerField(error_messages={"required": "单位不能为空  "})
    price = django_fields.DecimalField(max_digits=8, decimal_places=2, error_messages={"required": "单价不能为空",
                                                                                       "invalid": "请输入合法的价格"})
    total_price = django_fields.DecimalField(max_digits=8, decimal_places=2, error_messages={"required": "总价不能为空",
                                                                                       "invalid": "请输入合法的价格"})


class WastageForm(django_forms.Form):
    goods_id = django_fields.IntegerField(error_messages={"required": "所选商品不能为空"})
    amount = django_fields.IntegerField(error_messages={"required": "数量不能为空"})
    date = django_fields.DateField(error_messages={"required": "采购日期不能为空", "invalid": "日期格式错误"})
    unit_id = django_fields.IntegerField(error_messages={"required": "单位不能为空  "})
