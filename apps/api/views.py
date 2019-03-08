from rest_framework.response import Response
from rest_framework import viewsets, permissions
from api.serializers import *
from rbac.models import Role
# from personnel.models import StaffRole as Staff2Role
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
        self.perform_update(serializer)
        roles = request.data.get('roles',[])
        if roles:
            instance.staff.roles.set(roles)
            # instance.staff.roles.clear()
            # for i in roles:
            #     role = Role.objects.get(id=i)
            #     instance.staff.roles.add(role)
        else:
            instance.staff.roles.clear()
        return Response(serializer.data)


class UserLogViewSet(viewsets.ModelViewSet):
    queryset = UserLog.objects.all().order_by('id')
    serializer_class = UserLogSerializer
    permission_classes = (permissions.IsAuthenticated,)