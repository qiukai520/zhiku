from django.forms import fields as django_fields
from django.forms import forms as django_forms
from django.core.exceptions import ValidationError


class DepartmentForm(django_forms.Form):
    department = django_fields.CharField(error_messages={"required": "部门名称不能为空"})


class CompanyForm(django_forms.Form):
    company = django_fields.CharField(error_messages={"required": "公司名称不能为空"})


class JobRankForm(django_forms.Form):
    job_rank = django_fields.CharField(error_messages={"required": "职级名称不能为空"})


class JobTitlekForm(django_forms.Form):
    job_title = django_fields.CharField(error_messages={"required": "职称名称不能为空"})


class ProjectForm(django_forms.Form):
    project = django_fields.CharField(error_messages={"required": "项目名称不能为空"})