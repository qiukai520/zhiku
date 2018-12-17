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
    path("contact/detail", views.contact_detail, name="contact_detail"),
    path("goods", views.goods_list, name="goods_list"),
    path("goods/edit", views.goods_edit, name='goods_edit'),
    path("goods/code",views.search_goods, name="search_goods"),
    path("goods/repertory/add",views.add_repertory,name="add_repertory"),
    path("invent/repertory/delete", views.remove_repertory, name="remove_repertory"),
    path("g_category", views.goods_category_list, name="goods_category_list"),
    path("g_category/edit", views.goods_category_edit, name='goods_category_edit'),
    path("goods/detail", views.goods_detail, name="goods_detail"),
    path("goods/delete", views.goods_delete, name="goods_delete"),
    path("goods/price", views.goods_price, name="goods_price"),
    path("goods/price_compare",views.price_compare,name="price_compare"),
    path("g_unit", views.goods_unit_list, name="goods_unit_list"),
    path("g_unit/edit", views.goods_unit_edit, name='goods_unit_edit'),
    path("fetch_linkman",views.fetch_linkman,name="fetch_linkman"),
    path("price/detail", views.price_detail, name="price_detail"),
    path("memo/detail", views.memo_detail,name="memo_detail"),
    path("industry", views.industry_list, name="industry_list"),
    path("industry/edit", views.industry_edit, name='industry_edit'),
    path("invent", views.invent_list, name="invent_list"),
    path("invent/edit", views.InventViewSet.as_view(), name="invent_edit"),
    path("invent/detail", views.invent_detail, name="invent_detail"),
    path("invent/record",views.invent_record,name="invent_record"),
    path("purchase/detail", views.purchase_record, name="purchase_record"),
    path("wastage/detail", views.wastage_detail, name="wastage_detail"),
    path("purchase/edit",views.PurchaseViewSet.as_view(),name="purchase_edit"),
    path("invent/wastage/edit", views.WastageViewSet.as_view(), name="wastage_edit"),
    path("purchase/bind", views.purchase_bind, name="purchase_bind"),
    path("supplier", views.supplier_list, name="supplier_list"),
    path("supplier/edit", views.supplier_edit, name='supplier_edit'),
    path("s_category", views.supplier_category_list, name="supplier_category_list"),
    path("s_category/edit", views.supplier_category_edit, name='supplier_category_edit'),
    path("supplier/linkman", views.supplier_linkman, name='supplier_linkman'),
    path("linkman/detail", views.linkman_detail, name="linkman_detail"),
    path("supplier/contact", views.supplier_contact, name='supplier_contact'),
    path("supplier/retailers/edit",views.retailers_edit,name="retail_supplier_edit"),
    path("supplier/retailers", views.retailers_list, name="retail_supplier_list"),
    path("supplier/memo", views.supplier_memo, name='supplier_memo'),
    path("supplier/detail", views.supplier_detail, name='supplier_detail'),
    path("supplier/delete", views.supplier_delete, name="supplier_delete"),
    path("warehouses",views.warehouse_list, name="warehouse_list"),
    path("warehouse/edit", views.WarehouseViewSet.as_view(), name="warehouse_edit"),
    path("ware_location", views.ware_location_list, name="warelocation"),
    path("ware_location/edit",views.WareLocationViewSet.as_view(), name="warelocation_edit"),
    path("location",views.warehouse_location,name="warehouse_location"),
    path("upload_goods_photo", views.goods_photo, name="goods_photo"),
    path("upload_goods_code", views.goods_code, name="goods_code"),
    path("upload_linkman_photo", views.linkman_photo, name="linkman_photo"),
    path("upload_linkman_card", views.linkman_card, name="linkman_card"),
    path("upload_supplier_photo", views.supplier_photo, name="supplier_photo"),
    path("upload_supplier_licence", views.supplier_licence, name="supplier_licence"),
    path("upload_supplier_attach", views.supplier_attach, name="supplier_attach"),
    path("upload_goods_attach", views.goods_attach, name="goods_attach"),
    path("upload_linkman_attach", views.linkman_attach, name="linkman_attach"),
    path("upload_contact_attach", views.contact_attach, name="contact_attach"),
    path("goods/webuploader_photo.html",views.webuploader_photo,name="webuploader_photo"),
    path("goods/webuploader_photo_delete.html", views.webuploader_photo_detele, name="webuploader_photo_detele")
]
