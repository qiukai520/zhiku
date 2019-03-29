from django.urls import path
from . import views

urlpatterns = [
    path('assets', views.assets, name="assets"),
    path('assets/edit', views.assets_edit, name="assets_edit"),
    path('assets/detail', views.assets_detail, name="assets_detail"),
    path('assets/delete', views.assets_delete, name="assets_delete"),
    path('assets/detail/1', views.assets_detail_1, name="assets_detail_1"),
    path('assets/detail/2', views.assets_detail_2, name="assets_detail_2"),
    path('assets/detail/3', views.assets_detail_3, name="assets_detail_3")
]
