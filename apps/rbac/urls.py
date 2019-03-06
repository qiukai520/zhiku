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
from django.urls import path, re_path
from django.urls import path,re_path
from . import views

urlpatterns = [
    path(r'user_list/', views.get_user_list, name='user_list'),
    # path(r'group_list/', views.get_group_list, name='group_list'),
    path(r'create_user/', views.create_user, name='create_user'),
    path(r'user_center/', views.user_center, name='user_center'),
    re_path(r'reset_password/(?P<pk>[0-9]+)/', views.reset_password, name='reset_password'),
    re_path(r'change_password/(?P<pk>[0-9]+)/', views.change_password, name='change_password'),
    path(r'user_log/', views.get_user_log, name='user_log'),

]
