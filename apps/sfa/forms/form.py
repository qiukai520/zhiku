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
    age = django_fields.IntegerField(error_messages={"required": "年龄不能为空","invalid": "请输入有效整数"})


class MemoForm(django_forms.Form):
    customer_id = django_fields.IntegerField(error_messages={"required": "请选择客户"})
    title = django_fields.CharField(error_messages={"required": "标题不能为空"})
    detail = django_fields.CharField(error_messages={"required": "详细不能为空"})


class FollowForm(django_forms.Form):
    customer_id = django_fields.IntegerField(error_messages={"required": "请选择客户"})
    way_id = django_fields.IntegerField(error_messages={"required": "请选择跟踪方式"})
    contact_id = django_fields.IntegerField(error_messages={"required": "请选择联络方式"})
    linkman_id = django_fields.IntegerField(error_messages={"required": "请选择客户联系人"})
    result_id = django_fields.IntegerField(error_messages={"required": "请选择需求意向"})
    purpose_id = django_fields.IntegerField(error_messages={"required": "请选择客户需求"})
    date = django_fields.DateField(error_messages={"required":"跟进日期不能为空"})


class ContactForm(django_forms.Form):
    customer_id = django_fields.IntegerField(error_messages={"required": "请选择供应商"})
    category = django_fields.IntegerField(error_messages={"required": "请选择交易分类"})
    linkman_id = django_fields.IntegerField(error_messages={"required": "请选择联系人"})
    project = django_fields.CharField(error_messages={"required": "交易项目不能为空"})
    date = django_fields.DateField(error_messages={"required": "交易日期不能为空", "invalid": "日期格式错误"})


class RuleForm(django_forms.Form):
    rule = django_fields.IntegerField(error_messages={"required": "天数不能为空"})
