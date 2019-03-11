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

class Select_ProjectForm(django_forms.Form):
    name = django_fields.CharField(error_messages={"required": "项目名称不能为空"})


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

class PerformanceygForm(django_forms.Form):
    content = django_fields.CharField(error_messages={"required": "内容明细不能为空"}, max_length=128)
    effective_time = django_fields.DateTimeField(error_messages={"required": "生效时间不能为空", "invalid": "生效时间格式错误"})
    operator = django_fields.CharField(required=False)

class LaborContractForm(django_forms.Form):
    remark = django_fields.CharField(error_messages={"required": "备注不能为空"}, max_length=128)
    create_time = django_fields.DateTimeField(error_messages={"required": "劳动合同创建时间不能为空", "invalid": "劳动合同创建时间格式错误"})

class ReasonsLeaveForm(django_forms.Form):
    reasons = django_fields.CharField(error_messages={"required": "离职原因不能为空"}, max_length=128)
    reasons_time = django_fields.DateTimeField(error_messages={"required": "工资计算截止日期不能为空", "invalid": "工资截止日期创建格式错误"})
    reasons_bool1 = django_fields.BooleanField(required=False)
    reasons_bool2 = django_fields.BooleanField(required=False)
    reasons_id_id = django_fields.IntegerField(error_messages={"required": "请选择用品"})
    reasons_people_id = django_fields.IntegerField(error_messages={"required": "请选择工作交接人"})
    reasons_time1 = django_fields.DateTimeField(error_messages={"required": "离岗日期不能为空", "invalid": "离岗日期时间格式错误"})


class SocialSecurityForm(django_forms.Form):
    s_id = django_fields.CharField(error_messages={"required": "社保卡号不能为空"}, max_length=32)
    s_money = django_fields.DecimalField(error_messages={"required": "金额不能为空"}, max_digits=20, decimal_places=10)
    s_time = django_fields.DateField(error_messages={"required": "起始时间不能为空", "invalid": "起始时间格式错误"})
    s_remark = django_fields.CharField(required=False, max_length=128)

class SuppliesForm(django_forms.Form):
    supplies_id_id = django_fields.IntegerField(error_messages={"required": "请选择用品"})
    supplies_time = django_fields.DateField(error_messages={"required": "领用日时间不能为空", "invalid": "领用日时间格式错误"})
    supplies_remark = django_fields.CharField(error_messages={"required": "备注不能为空"}, max_length=128)





