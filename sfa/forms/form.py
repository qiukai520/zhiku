from .validate_func import *
from django.forms import fields as django_fields
from django.forms import forms as django_forms


class CustomerForm(django_forms.Form):
    category_id = django_fields.IntegerField(error_messages={"required": "请选择商品分类"})
    company = django_fields.CharField(error_messages={"required": "公司名称不能为空"})
    town_id = django_fields.IntegerField(min_value=1 , error_messages={"required": "请选择街道","min_value":"请选择街道"})
    business = django_fields.CharField(error_messages={"required": "主营业务不能为空"})