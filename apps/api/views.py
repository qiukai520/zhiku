from rest_framework.response import Response
from rest_framework import viewsets, permissions
from api.serializers import *
from rbac.models import Role,User2Role
# Create your views here.


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UsersSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def update(self,request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        roles = request.data.get('roles',[])
        if roles:
            User2Role.objects.filter(user=instance.id).delete()
            for i in roles:
                role = Role.objects.get(id=i)
                User2Role.objects.create(user=instance, role=role)
        else:
            User2Role.objects.filter(user=instance.id).delete()
        return Response(serializer.data)



class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all().order_by('id')
    serializer_class = PermissionSerializer
    permission_classes = (permissions.IsAuthenticated,)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('id')
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticated,)


class UserLogViewSet(viewsets.ModelViewSet):
    queryset = UserLog.objects.all().order_by('id')
    serializer_class = UserLogSerializer
    permission_classes = (permissions.IsAuthenticated,)