from .validate_func import *
from django.forms import fields as django_fields
from django.forms import forms as django_forms



class DepartmentForm(django_forms.Form):
    department = django_fields.CharField(error_messages={"required": "部门名称不能为空"})


class CompanyForm(django_forms.Form):
    company = django_fields.CharField(error_messages={"required": "公司名称不能为空"})


class JobRankForm(django_forms.Form):
    rank = django_fields.CharField(error_messages={"required": "职级名称不能为空"})


class JobTitlekForm(django_forms.Form):
    job_title = django_fields.CharField(error_messages={"required": "职称名称不能为空"})


class ProjectForm(django_forms.Form):
    project = django_fields.CharField(error_messages={"required": "项目名称不能为空"})


class StaffForm(django_forms.Form):
    job_number = django_fields.CharField(error_messages={"required": "工号不能为空"}, max_length=32)
    name = django_fields.CharField(error_messages={"required":"员工姓名不能为空"},max_length=16)
    gender = django_fields.IntegerField(error_messages={"required":"性别不能为空"})
    phone = django_fields.CharField(validators=[mobile_validate,], error_messages={"required":"手机号码不能为空"},max_length=11)
    email = django_fields.EmailField(required=False,error_messages={"invalid" : "邮箱格式错误"},max_length=32)
    birthday = django_fields.DateField(error_messages={"required": "生日不能为空","invalid": "生日日期格式错误"})
    hire_day = django_fields.DateField(error_messages={"required": "入职日期不能为空","invalid": "入职日期格式错误"})
    native_place = django_fields.CharField(required=False,max_length=16)
    nationality = django_fields.CharField(required=False,max_length=32)
    family_address = django_fields.CharField(required=False,max_length=128)
    current_address = django_fields.CharField(required=False,max_length=128)
    education = django_fields.CharField(required=False,max_length=32)
    id_card = django_fields.CharField(validators=[Idcard_validate,], required=False,max_length=18)
    bank = django_fields.CharField(required=False,max_length=32)
    bank_account = django_fields.CharField(validators=[bankAccount_validate], required=False,max_length=32)
    account_name = django_fields.CharField(required=False,max_length=32)
    contact_phone = django_fields.CharField(validators=[mobile_validate,],required=False,max_length=11)
    contact_man = django_fields.CharField(required=False,max_length=32)
    contact_relation = django_fields.CharField(required=False,max_length=16)
    recruit_channel = django_fields.CharField(required=False,max_length=16)
    referrer = django_fields.CharField(required=False,max_length=16)
    remark = django_fields.CharField(required=False,max_length=128)



