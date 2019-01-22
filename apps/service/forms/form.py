from django.forms import fields as django_fields
from django.forms import forms as django_forms


class FollowForm(django_forms.Form):
    contract_id = django_fields.IntegerField(error_messages={"required": "请选择合同"})
    way_id = django_fields.IntegerField(error_messages={"required": "请选择跟踪方式"})
    contact_id = django_fields.IntegerField(error_messages={"required": "请选择联络方式"})
    linkman_id = django_fields.IntegerField(error_messages={"required": "请选择客户联系人"})
    date = django_fields.DateField(error_messages={"required":"跟进日期不能为空"})


class WayForm(django_forms.Form):
    content = django_fields.CharField(error_messages={"required":"跟进方式不能为空"})


class ContactForm(django_forms.Form):
    content = django_fields.CharField(error_messages={"required": "联络方式不能为空"})
