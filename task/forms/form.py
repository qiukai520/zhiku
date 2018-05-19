from django.forms import fields as django_fields
from django.forms import forms as django_forms
from django.core.exceptions import ValidationError


class TaskForm(django_forms.Form):
    title = django_fields.CharField(error_messages={"required": "任务名称不能为空"})
    content = django_fields.CharField(error_messages={"required": "任务描述不能为空"})
    type_id = django_fields.IntegerField(required=False)
    tcid = django_fields.IntegerField(required=False)
    issuer_id = django_fields.IntegerField(required=False)
    perfor_id = django_fields.IntegerField(required=False)
    tags = django_fields.CharField(required=False)
    attachment = django_fields.CharField(required=False)
    start_time = django_fields.CharField(required=False)
    deadline = django_fields.DateTimeField(required=False)
    reviewers = django_fields.CharField(error_messages={"required": "审核人不能为空"})


class PerformForm(django_forms.Form):
    name = django_fields.CharField(error_messages={"required": "绩效名称不能为空"})
    personal_score = django_fields.IntegerField(error_messages={'required': '个人分值不能为空', 'invalid': '请输入有效整数'})
    personal_total = django_fields.IntegerField(error_messages={'required': '个人总分不能为空', 'invalid': '请输入有效整数'})
    team_score = django_fields.IntegerField(error_messages={'required': '团队分值不能为空', 'invalid': '请输入有效整数'})
    team_total = django_fields.IntegerField(error_messages={'required': '团队总分不能为空', 'invalid': '请输入有效整数'})


class TaskAssignForm(django_forms.Form):
    title = django_fields.CharField(error_messages={"required": "标题不能为空"})
    content = django_fields.CharField(error_messages={'required': '任务内容不能为空'})
    attachment = django_fields.CharField(required=False)
    # deadline = django_fields.DateTimeField(required=False)
