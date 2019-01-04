"""thinking_library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import xadmin
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("products", views.product_list, name="products"),
    path("product/edit", views.product_edit, name='product_edit'),
    path("locations", views.location_list, name="locations"),
    path("location/edit", views.location_edit, name='location_edit'),
    path("meals", views.meals, name="meals"),
    path("meal/edit", views.meal_edit, name='meal_edit'),
    path("meals/delete", views.meals_delete, name="meals_delete"),
    path("fetch_meal", views.fetch_meal,name="fetch_meal"),
    path("contract_edit", views.customer_contract, name="customer_contract"),
    path("contracts",views.contracts_list,name="contract_list"),
    path("contract/payment", views.add_payment, name="add_payment"),
    path("contracts_center", views.contracts_center, name="contracts_center"),
    path("unapproved", views.contract_approve, name="unapproved"),
    path("product_meal",views.product_meal,name="product_meal"),
    path("approvers",views.approver_list, name="approvers"),
    path("approver/edit",views.approver_edit,name="approver_edit"),
    path("approve", views.approve, name="approve"),
    path("approve/detail", views.approve_detail, name="approve_detail"),
    path("approve/record", views.approve_record,  name="approved_record_detail"),
    path("payment/detail",views.payment_detail,name="payment_detail"),
    path("contract/detail",views.contract_detail,name="contract_detail"),
    path("upload_attach", views.contract_attach, name="contract_attach"),


]
