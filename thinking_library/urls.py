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
from django.urls import path,include
from task import views as task_view
from personnel import views as p_view
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    path('index/', task_view.index, name='index'),
    path('login/', task_view.login, name='login'),
    path('logout/', task_view.logout, name='logout'),
    path("task/", include('task.urls')),
    path("personnel/", include('personnel.urls')),
    path("inventory/", include('inventory.urls')),
    path("sfa/", include('sfa.urls')),
    path("public/", include('public.urls')),
    path('attachment_upload.html', task_view.attachment_upload, name='attachment_upload'),
    path("attachment_download.html", task_view.attachment_download, name="attachment_download"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # 配置media
