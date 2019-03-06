from django.urls import path, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()

router.register(r'users', views.UsersViewSet)
# router.register(r'permission', views.PermissionViewSet)
# router.register(r'group', views.GroupViewSet)
router.register(r'user_log', views.UserLogViewSet)


urlpatterns = [
    path(r'', include(router.urls)),
    path(r'api/', include('rest_framework.urls', namespace='rest_framework'))
]
