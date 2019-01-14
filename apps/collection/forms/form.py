from .validate_func import *
from django.forms import fields as django_fields
from django.forms import forms as django_forms


class KnowledgeForm(django_forms.Form):
    relate_title = django_fields.CharField(error_messages={"required":"工单标题为空"})
    type_id = django_fields.IntegerField(error_messages={"required":"归档分类不能为空"})
    title = django_fields.CharField(error_messages={"required":"标题不能为空"})
    summary = django_fields.CharField(error_messages={"required":"小结不能为空"})


