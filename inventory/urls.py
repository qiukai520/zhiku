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

    path("city", views.city_list, name="city_list"),
    path("city_edit", views.city_edit, name='city_edit'),
    path("city_country",views.city_country, name="city_country"),
    path("contact_detail", views.contact_detail, name="contact_detail"),
    path("town", views.town_list, name="town_list"),
    path("town_edit", views.town_edit, name='town_edit'),
    path("country", views.country_list, name="country_list"),
    path("country_edit", views.country_edit, name='country_edit'),
    path("country_town", views.country_town, name='country_town'),
    path("goods", views.goods_list, name="goods_list"),
    path("goods_edit", views.goods_edit, name='goods_edit'),
    path("goods_category", views.goods_category_list, name="goods_category_list"),
    path("goods_category_edit", views.goods_category_edit, name='goods_category_edit'),
    path("goods_detail", views.goods_detail, name="goods_detail"),
    path("goods_delete", views.goods_delete, name="goods_delete"),
    path("goods_price", views.goods_price, name="goods_price"),
    path("price_compare",views.price_compare,name="price_compare"),
    path("goods_unit", views.goods_unit_list, name="goods_unit_list"),
    path("goods_unit_edit", views.goods_unit_edit, name='goods_unit_edit'),
    path("fetch_linkman",views.fetch_linkman,name="fetch_linkman"),
    path("linkman_detail", views.linkman_detail, name="linkman_detail"),
    path("price_detail", views.price_detail, name="price_detail"),
    path("memo_detail", views.memo_detail,name="memo_detail"),
    path("nation", views.nation_list, name="nation_list"),
    path("nation_edit", views.nation_edit, name='nation_edit'),
    path("nation_province", views.nation_province, name='nation_province'),
    path("province_city", views.province_city, name='province_city'),
    path("province", views.province_list, name='province_list'),
    path("province_edit", views.province_edit, name='province_edit'),
    path("industry", views.industry_list, name="industry_list"),
    path("industry_edit", views.industry_edit, name='industry_edit'),
    path("invent", views.invent_list, name="invent_list"),
    path("invent_edit", views.InventViewSet.as_view(), name="invent_edit"),
    path("invent_detail", views.invent_detail, name="invent_detail"),
    path("invent_record",views.invent_record,name="invent_record"),
    path("purchase_record", views.purchase_record, name="purchase_record"),
    path("purchase_edit",views.PurchaseViewSet.as_view(),name="purchase_edit"),
    path("purchase_bind", views.purchase_bind, name="purchase_bind"),
    path("supplier", views.supplier_list, name="supplier_list"),
    path("supplier_edit", views.supplier_edit, name='supplier_edit'),
    path("supplier_category", views.supplier_category_list, name="supplier_category_list"),
    path("supplier_category_edit", views.supplier_category_edit, name='supplier_category_edit'),
    path("supplier_linkman", views.supplier_linkman, name='supplier_linkman'),
    path("supplier_contact", views.supplier_contact, name='supplier_contact'),
    path("retail_supplier_edit",views.retail_supplier_edit,name="retail_supplier_edit"),
    path("retail_supplier_list", views.retail_supplier_list, name="retail_supplier_list"),
    path("supplier_memo", views.supplier_memo, name='supplier_memo'),
    path("supplier_detail", views.supplier_detail, name='supplier_detail'),
    path("supplier_delete", views.supplier_delete, name="supplier_delete"),
    path("warehouses",views.warehouse_list, name="warehouse_list"),
    path("warehouse_edit", views.WarehouseViewSet.as_view(), name="warehouse_edit"),
    path("warelocation", views.ware_location_list, name="warelocation"),
    path("warelocation_edit",views.WareLocationViewSet.as_view(), name="warelocation_edit"),
    path("warehouse_location",views.warehouse_location,name="warehouse_location"),
    path("upload_goods_photo", views.goods_photo, name="goods_photo"),
    path("upload_goods_code", views.goods_code, name="goods_code"),
    path("upload_linkman_photo", views.linkman_photo, name="linkman_photo"),
    path("upload_linkman_card", views.linkman_card, name="linkman_card"),
    path("upload_supplier_photo", views.supplier_photo, name="supplier_photo"),
    path("upload_supplier_licence", views.supplier_licence, name="supplier_licence"),
    path("upload_attach", views.supplier_attach, name="supplier_attach"),
    path("upload_attach", views.goods_attach, name="goods_attach"),
    path("upload_attach", views.linkman_attach, name="linkman_attach"),
    path("upload_attach", views.contact_attach, name="contact_attach"),
    path("webuploader_photo.html",views.webuploader_photo,name="webuploader_photo"),
    path("webuploader_photo_delete.html", views.webuploader_photo_detele, name="webuploader_photo_detele")


]
