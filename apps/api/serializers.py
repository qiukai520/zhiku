from rest_framework import serializers
from django.contrib.auth.models import Permission, Group
from rbac.models import User
from rbac.models import UserLog
# from personnel.models import StaffRole as Staff2Role


class UsersSerializer(serializers.ModelSerializer):

    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id','username','is_active',"roles",)
        read_only_fields = ('is_superuser',"is_staff")

    def get_roles(self, obj):
        # 获取用户角色
        queryset = obj.staff.roles.all()
        return [row.id for row in queryset]


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'title')


class User2RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'user',"role")


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('id', 'name')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'user_set', 'permissions')


class UserLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLog
        fields = '__all__'

