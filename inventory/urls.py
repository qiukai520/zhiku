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
    path("nation", views.nation_list, name="nation_list"),
    path("nation_edit", views.nation_edit, name='nation_edit'),
    path("province", views.province_list, name="province_list"),
    path("province_edit", views.province_edit, name='province_edit'),
    path("industry", views.industry_list, name="industry_list"),
    path("industry_edit", views.industry_edit, name='industry_edit'),
    path("supplier_category", views.supplier_category_list, name="supplier_category_list"),
    path("supplier_category_edit", views.supplier_category_edit, name='supplier_category_edit'),
    path("goods_category", views.goods_category_list, name="goods_category_list"),
    path("goods_category_edit", views.goods_category_edit, name='goods_category_edit'),

    path("supplier", views.supplier_list, name="supplier_list"),
    path("supplier_edit", views.supplier_edit, name='supplier_edit'),
    # path("staff_delete",views.staff_delete,name="staff_delete"),
    # path("upload_life_photo", views.life_photo, name="life_photo"),
    # path("upload_attach", views.staff_attach, name="staff_attach"),

]
