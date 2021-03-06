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
from . import tasks

urlpatterns = [
    path("customer", views.customer, name="customer_list"),
    path("center", views.customer_center, name="customer_center"),
    path("public", views.customer_public, name="customer_public"),
    path("sea_rule", views.sea_rule_list, name="sea_rule_list"),
    path("sea_rule/edit",views.sea_rule_edit,name="sea_rule_edit"),
    path("customer/edit", views.customer_edit,name="customer_edit"),
    path("customer/delete",views.customer_delete,name="customer_delete"),
    path("customer/detail", views.customer_detail, name='customer_detail'),
    path("customer/linkman", views.customer_linkman, name='customer_linkman'),
    path("customer/linkman/detail", views.c_linkman_detail, name='c_linkman_detail'),
    path("customer/follow/detail", views.c_folllow_detail, name='c_follow_detail'),
    path("customer/contact/detail",views.c_contact_detail,name="c_contact_detail"),
    path("customer/memo/detail", views.c_memo_detail, name='c_memo_detail'),
    path("customer/memo", views.customer_memo, name='customer_memo'),
    path("customer/contact",views.customer_contact,name="customer_contact"),
    path("linkman/delete", views.linkman_delete, name="customer_linkman_delete"),
    path("contact/delete", views.contact_delete, name="customer_contact_delete"),
    path("follow/delete", views.follow_delete, name="customer_follow_delete"),
    path("memo/delete", views.memo_delete, name="customer_memo_delete"),
    path("customer/follow", views.customer_follow, name='customer_follow'),
    path("customer/assign", views.customer_assign, name='customer_assign'),
    path("follow_customer",views.follow_customer, name="follow_customer"),
    path("abandon_customer", views.abandon_customer, name="abandon_customer"),
    path("upload_customer_photo", views.customer_photo, name="customer_photo"),
    path("upload_customer_licence", views.customer_licence, name="customer_licence"),
    path("upload_attach", views.customer_attach, name="customer_attach"),



]
