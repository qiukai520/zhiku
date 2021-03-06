from django.forms import fields as django_fields
from django.forms import forms as django_forms
from django.core.exceptions import ValidationError


class TaskForm(django_forms.Form):
    title = django_fields.CharField(max_length=128,error_messages={"required": "任务名称不能为空"})
    content = django_fields.CharField(error_messages={"required": "任务描述不能为空"})
    type_id = django_fields.IntegerField(error_messages={"required": "归档分类不能为空"})
    issuer_id = django_fields.IntegerField(required=False)
    tags = django_fields.CharField(required=False)
    attachment = django_fields.CharField(required=False)


class TaskMapForm(django_forms.Form):
    cycle_id = django_fields.IntegerField(error_messages={"required": "任务周期不能为空"})
    assigner_id = django_fields.IntegerField(required=False)
    perfor_id = django_fields.IntegerField(required=False)
    start_time = django_fields.CharField(error_messages={"required": "起始时间不能为空"})
    team = django_fields.IntegerField(error_messages={"required": "任务方式不能为空"})
    deadline = django_fields.DateTimeField(error_messages={"required": "终止日期"})
    reviewers = django_fields.CharField(error_messages={"required": "请选择审核人"})
    assigners = django_fields.CharField(error_messages={"required": "请选择指派对象"})


class PerformForm(django_forms.Form):
    name = django_fields.CharField(error_messages={"required": "绩效名称不能为空"})
    personal_score = django_fields.IntegerField(error_messages={'required': '个人分值不能为空', 'invalid': '请输入有效整数'})
    personal_total = django_fields.IntegerField(error_messages={'required': '个人总分不能为空', 'invalid': '请输入有效整数'})
    team_score = django_fields.IntegerField(error_messages={'required': '团队分值不能为空', 'invalid': '请输入有效整数'})
    team_total = django_fields.IntegerField(error_messages={'required': '团队总分不能为空', 'invalid': '请输入有效整数'})


class TaskSortForm(django_forms.Form):
    name = django_fields.CharField(error_messages={"required": "分类名称不能为空"})


class DepartmentForm(django_forms.Form):
    department = django_fields.CharField(error_messages={"required": "部门名称不能为空"})


class TaskAssignForm(django_forms.Form):
    title = django_fields.CharField(error_messages={"required": "标题不能为空"})
    content = django_fields.CharField(error_messages={'required': '任务内容不能为空'})
    attachment = django_fields.CharField(required=False)
    deadline = django_fields.DateTimeField(error_messages={"required": "截止日期不能为空"})


class CompleteTaskForm(django_forms.Form):
    title = django_fields.CharField(error_messages={"required": "标题不能为空"})
    summary = django_fields.CharField(error_messages={'required': '任务小结不能为空'})
    attachment = django_fields.CharField(required=False)


class TaskReviewForm(django_forms.Form):
    is_complete = django_fields.IntegerField(error_messages={"required": "审核状态不能为空"})
    reason = django_fields.CharField(required=False)
    evaluate = django_fields.FloatField(required=False)


class LoginForm(django_forms.Form):
    username = django_fields.CharField(error_messages={"required":"用户名不能为空"})
    password = django_fields.CharField(error_messages={"required":"密不能为空"})