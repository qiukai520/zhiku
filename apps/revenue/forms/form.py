from .validate_func import *
from django.forms import fields as django_fields
from django.forms import forms as django_forms


class IncomeClassifyForm(django_forms.Form):
    name = django_fields.CharField(error_messages={"required": "收入分类不能为空"})

class AssociatesForm(django_forms.Form):
    name = django_fields.CharField(error_messages={"required": "关联人不能为空"})

class Approver2Form(django_forms.Form):
    name = django_fields.CharField(error_messages={"required": "审批人不能为空"})

class Approver3Form(django_forms.Form):
    name = django_fields.CharField(error_messages={"required": "审批人不能为空"})

class RevenueForm(django_forms.Form):
    company_id = django_fields.IntegerField(error_messages={"required": "请选择公司"})
    project_id = django_fields.IntegerField(error_messages={"required": "请选择项目"})
    income_name = django_fields.CharField(error_messages={"required": "收入名称不能为空"}, max_length=64)
    income_classify_id = django_fields.IntegerField(error_messages={"required": "收入分类"})
    number = django_fields.CharField(error_messages={"required": "存档编号不能为空"}, max_length=64)
    coordinate = django_fields.CharField(error_messages={"required": "存档坐标不能为空"}, max_length=64)
    money = django_fields.DecimalField(error_messages={"required": "金额不能为空"}, max_digits=20, decimal_places=5)
    associates_id = django_fields.IntegerField(error_messages={"required": "请选择关联人"})
    approver_id = django_fields.IntegerField(error_messages={"required": "请选择审批人"})
    income_time = django_fields.DateTimeField(error_messages={"required": "收入日期不能为空", "invalid": "收入日期时间格式错误"})
    remark = django_fields.CharField(required=False, max_length=128)

class DisbursementForm(django_forms.Form):
    company_id = django_fields.IntegerField(error_messages={"required": "请选择公司"})
    project_id = django_fields.IntegerField(error_messages={"required": "请选择项目"})
    disbursement_name = django_fields.CharField(error_messages={"required": "支出名称不能为空"}, max_length=64)
    classify_id = django_fields.IntegerField(error_messages={"required": "支出分类"})
    number = django_fields.CharField(error_messages={"required": "存档编号不能为空"}, max_length=64)
    coordinate = django_fields.CharField(error_messages={"required": "存档坐标不能为空"}, max_length=64)
    money = django_fields.DecimalField(error_messages={"required": "金额不能为空"}, max_digits=20, decimal_places=5)
    associates_id = django_fields.IntegerField(error_messages={"required": "请选择关联人"})
    approver_id = django_fields.IntegerField(error_messages={"required": "请选择审批人"})
    disbursement_time = django_fields.DateTimeField(error_messages={"required": "支出日期不能为空", "invalid": "支出日期时间格式错误"})
    remark = django_fields.CharField(required=False, max_length=128)


