# -*- coding: utf-8 -*-
'''
@File  : practice.py
@Author: Lee
@Date  : 2018/11/7 10:21
'''

__author__ = 'lizhihong'

#独立使用django的model
import sys
import os

pwd = os.path.dirname(os.path.abspath(__file__))

sys.path.append(pwd+"../")
# 加载配置文件
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "thinking_library.settings")


import django
django.setup()

from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

class ListUsers(APIView):
    """
    列出系统中的所有用户的视图。

    * 需要token认证
    * 只有管理员用户可以访问这个视图。
    """
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAdminUser,)

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        usernames = [user.username for user in User.objects.all()]
        return Response(usernames)


from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .models import User


class UserViewSet(ModelViewSet):
    def create(self, request, *args, **kwargs):
        self.serializer_class = UserCreateSerializer
        data = request.data.dict()
        serializer = UserCreateSerializer(data=data)
        if not serial.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        pass

    def update(self, request, *args, **kwargs):
        pass

    def list(self, request, *args, **kwargs):
        self.serializer_class = UserListSerializer
        self.queryset = User.objects.all()
        return super(UserViewSet, self).list(request)

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk', 1)
        self.serializer_class = UserDetailSerializer
        self.queryset = User.objects.filter(pk=pk)
        return super(UserViewSet, self).retrieve(request)




