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
    path("customer", views.customer_list, name="customer_list"),
    path("customer/edit",views.customer_edit,name="customer_edit"),
    path("upload_customer_photo", views.customer_photo, name="customer_photo"),
    path("upload_customer_licence", views.customer_licence, name="customer_licence"),
    path("upload_attach", views.customer_attach, name="customer_attach"),
]
