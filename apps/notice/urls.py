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
    path('',views.notice_view,name='noticeview'),
    path('list/',views.notice_table_list,name='noticelist'),
    path('action/',views.notice_action,name='noticeaction'),
    path('readall/',views.notice_readall,name='noticereadall'),
    path('count/',views.notice_count,name='noticecount'),
    path('read/<str:notice_id>/',views.notice_read,name='noticeread'),
]