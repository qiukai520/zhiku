from .validate_func import *
from django.forms import fields as django_fields
from django.forms import forms as django_forms


class CustomerForm(django_forms.Form):
    category_id = django_fields.IntegerField(error_messages={"required": "请选择商品分类"})
    company = django_fields.CharField(error_messages={"required": "公司名称不能为空"})
    town_id = django_fields.IntegerField(min_value=1 , error_messages={"required": "请选择街道","min_value":"请选择街道"})
    business = django_fields.CharField(error_messages={"required": "主营业务不能为空"})


class LinkmanForm(django_forms.Form):
    customer_id = django_fields.IntegerField(error_messages={"required": "请选择客户"})
    name = django_fields.CharField(error_messages={"required": "联系人姓名不能为空"})
    birthday = django_fields.DateField(error_messages={"required": "生日不能为空", "invalid": "生日日期格式错误"})


class MemoForm(django_forms.Form):
    customer_id = django_fields.IntegerField(error_messages={"required": "请选择客户"})
    title = django_fields.CharField(error_messages={"required": "标题不能为空"})
    detail = django_fields.CharField(error_messages={"required": "详细不能为空"})