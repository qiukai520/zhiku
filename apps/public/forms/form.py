from .validate_func import *
from django.forms import fields as django_fields
from django.forms import forms as django_forms


class NationForm(django_forms.Form):
    nation = django_fields.CharField(error_messages={"required": "国家名称不能为空"})


class ProvinceForm(django_forms.Form):
    province = django_fields.CharField(error_messages={"required": "省份不能为空"})
    nation_id = django_fields.IntegerField(error_messages={"required":"请选择国家"})


class CityForm(django_forms.Form):
    city = django_fields.CharField(error_messages={"required": "城市不能为空"})
    province_id = django_fields.IntegerField(error_messages={"required":"请选择省份"})


class CountryForm(django_forms.Form):
    country = django_fields.CharField(error_messages={"required": "县区不能为空"})
    city_id = django_fields.IntegerField(error_messages={"required": "请选择城市"})


class TownForm(django_forms.Form):
    town = django_fields.CharField(error_messages={"required": "街道不能为空"})
    country_id = django_fields.IntegerField(error_messages={"required": "请选择县(区)","invalid": "请输入合法的县(区)"})
