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
    path("contact_detail", views.contact_detail, name="contact_detail"),
    path("goods", views.goods_list, name="goods_list"),
    path("goods/edit", views.goods_edit, name='goods_edit'),
    path("goods/code",views.search_goods, name="search_goods"),
    path("repertory/add",views.add_repertory,name="add_repertory"),
    path("repertory/delete", views.remove_repertory, name="remove_repertory"),
    path("goods_category", views.goods_category_list, name="goods_category_list"),
    path("goods_category_edit", views.goods_category_edit, name='goods_category_edit'),
    path("goods/detail", views.goods_detail, name="goods_detail"),
    path("goods/delete", views.goods_delete, name="goods_delete"),
    path("goods/price", views.goods_price, name="goods_price"),
    path("price/compare",views.price_compare,name="price_compare"),
    path("goods_unit", views.goods_unit_list, name="goods_unit_list"),
    path("goods_unit_edit", views.goods_unit_edit, name='goods_unit_edit'),
    path("fetch_linkman",views.fetch_linkman,name="fetch_linkman"),
    path("linkman_detail", views.linkman_detail, name="linkman_detail"),
    path("price_detail", views.price_detail, name="price_detail"),
    path("memo_detail", views.memo_detail,name="memo_detail"),
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
    path("supplier/edit", views.supplier_edit, name='supplier_edit'),
    path("supplier_category", views.supplier_category_list, name="supplier_category_list"),
    path("supplier_category_edit", views.supplier_category_edit, name='supplier_category_edit'),
    path("supplier/linkman", views.supplier_linkman, name='supplier_linkman'),
    path("supplier/contact", views.supplier_contact, name='supplier_contact'),
    path("retail_supplier_edit",views.retail_supplier_edit,name="retail_supplier_edit"),
    path("retail_supplier_list", views.retail_supplier_list, name="retail_supplier_list"),
    path("supplier/memo", views.supplier_memo, name='supplier_memo'),
    path("supplier/detail", views.supplier_detail, name='supplier_detail'),
    path("supplier/delete", views.supplier_delete, name="supplier_delete"),
    path("warehouses",views.warehouse_list, name="warehouse_list"),
    path("warehouse/edit", views.WarehouseViewSet.as_view(), name="warehouse_edit"),
    path("warelocation", views.ware_location_list, name="warelocation"),
    path("warelocation/edit",views.WareLocationViewSet.as_view(), name="warelocation_edit"),
    path("warehouse_location",views.warehouse_location,name="warehouse_location"),
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
    path("webuploader_photo_delete.html", views.webuploader_photo_detele, name="webuploader_photo_detele")
]
