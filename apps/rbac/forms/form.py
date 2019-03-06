from django.forms import fields as django_fields
from django.forms import forms as django_forms
from django.core.exceptions import ValidationError

class LoginForm(django_forms.Form):
    username = django_fields.CharField(error_messages={"required":"用户名不能为空"})
    password = django_fields.CharField(error_messages={"required":"密骂不能为空"})


class PwdForm(django_forms.Form):
    raw_pwd = django_fields.CharField(error_messages={"required":"原始密不能为空"})
    new_pwd = django_fields.CharField(error_messages={"required":"新密码不能为空"})
    check_pwd = django_fields.CharField(error_messages={"required":"确认密码不能为空"})