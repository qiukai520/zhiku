from .validate_func import *
from django.forms import fields as django_fields
from django.forms import forms as django_forms

class AssetsForm(django_forms.Form):
    name = django_fields.CharField(error_messages={"required": "名称不能为空"}, max_length=15)
    assets_classify_id = django_fields.IntegerField(error_messages={"required": "请选择分类"})
    save_number = django_fields.CharField(error_messages={"required": "存档编号不能为空"}, max_length=32)
    save_coordinate_id = django_fields.IntegerField(error_messages={"required": "请选择存档坐标"})
    quantity = django_fields.DecimalField(error_messages={"required": "数量不能为空"}, max_digits=20, decimal_places=0)
    procurement_time = django_fields.DateTimeField(error_messages={"required": "采购日期", "invalid": "采购日期时间格式错误"})
    procurement_money = django_fields.DecimalField(error_messages={"required": "采购金额不能为空"}, max_digits=8, decimal_places=2)
    procurement_name_id = django_fields.IntegerField(error_messages={"required": "请选择采购人"})
    invoice = django_fields.CharField(error_messages={"required": "发票不能为空"})
    user_name_id = django_fields.IntegerField(error_messages={"required": "请选择使用人"})
    evidence = django_fields.CharField(required=False, max_length=32)
    evidence_number = django_fields.CharField(required=False, max_length=32)
    company_id = django_fields.IntegerField(error_messages={"required": "请选择隶属公司"})
    project_id = django_fields.IntegerField(error_messages={"required": "请选择隶属项目"})
    assets_status_id = django_fields.IntegerField(error_messages={"required": "请选择资产状态"})
    approver_id = django_fields.IntegerField(error_messages={"required": "请选择审批人"})
    remark = django_fields.CharField(required=False, max_length=128)

class AssetsClassifyForm(django_forms.Form):
    name = django_fields.CharField(error_messages={"required": "分类不能为空"})

class SaveCoordinateForm(django_forms.Form):
    name = django_fields.CharField(error_messages={"required": "存档坐标不能为空"})

class ProcurementNameForm(django_forms.Form):
    name = django_fields.CharField(error_messages={"required": "采购人不能为空"})

class UserNameForm(django_forms.Form):
    name = django_fields.CharField(error_messages={"required": "使用人不能为空"})

class AssetsStatusForm(django_forms.Form):
    name = django_fields.CharField(error_messages={"required": "资产状态不能为空"})



