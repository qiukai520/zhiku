# -*- coding: utf-8 -*-
from django.urls import path
from .views import *


urlpatterns = [
    #读取首页
    path('', PostViews.as_view(), name='posts'),
    path('more/', MoreViews.as_view(), name='more'),

]
