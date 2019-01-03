from .validate_func import *
from django.forms import fields as django_fields
from django.forms import forms as django_forms


class ProductForm(django_forms.Form):
    name = django_fields.CharField(error_messages={"required": "产品名称不能为空"})


class LocationForm(django_forms.Form):
    location = django_fields.CharField(error_messages={"required": "坐标位置不能为空"})


class MealForm(django_forms.Form):
    product_id = django_fields.IntegerField(min_value=1, error_messages={"required": "请选择产品","min_value":"请选择产品"})
    year_limit = django_fields.IntegerField(error_messages={"required": "请输入年限","invalid": "请输入合法的数字"})
    price = django_fields.DecimalField(max_digits=8, decimal_places=2, error_messages={"required": "请输入价格",
                                                                                            "invalid": "请输入合法的价格"})
    name = django_fields.CharField(error_messages={"required": "套餐名称不能为空"})
    standard = django_fields.CharField(error_messages={"required": "规格不能为空"})


class ContractForm(django_forms.Form):
    identifier = django_fields.CharField(error_messages={"required": "请填写合同编号"})
    receivable = django_fields.DecimalField(error_messages={"required": "请填写应收金额", "min_value" :"请填写合法的金额"})
    customer_id = django_fields.IntegerField(min_value=1, error_messages={"required": "签约客户不能为空", "min_value":"请选择产品"})
    product_id = django_fields.IntegerField(min_value=1, error_messages={"required": "请选择产品", "min_value":"请选择产品"})
    product_meal_id = django_fields.IntegerField(min_value=1, error_messages={"required": "请选择套餐","min_value":"请选择套餐"})
    sign = django_fields.DateField(error_messages={"required": "签约时间不能为空", "invalid": "签约日期格式错误"})
    end_date = django_fields.DateField(error_messages={"required": "生效时间不能为空", "invalid": "生效时间格式错误"})
    start_date = django_fields.DateField(error_messages={"required": "到期时间不能为空", "invalid": "到期时间格式错误"})
    # received = django_fields.DecimalField(error_messages={"invalid": "已收金额不合法"})
    # pending = django_fields.DecimalField(error_messages={"invalid": "待收金额不合法"})


class PaymentForm(django_forms.Form):
    contract_id = django_fields.IntegerField(min_value=1, error_messages={"required": "请选择合同", "min_value":"请选择合同"})
    payment = django_fields.DecimalField(error_messages={"required":"收款金额不能为空", "invalid": "收款金额不合法"})


