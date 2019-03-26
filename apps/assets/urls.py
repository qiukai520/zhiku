from django.urls import path
from . import views

urlpatterns = [
    path('assets', views.assets, name="assets"),
    path('assets/edit', views.assets_edit, name="assets_edit"),
    path('assets/detail', views.assets_detail, name="assets_detail"),
    path('assets/delete', views.assets_delete, name="assets_delete")
]
