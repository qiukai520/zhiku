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
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from task import views as task_view
from rbac.views import LoginView,logout
from personnel import views as p_view

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    path('index/', task_view.index, name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout, name='logout'),
    path("task/", include('task.urls')),
    path("personnel/", include('personnel.urls')),
    path("inventory/", include('inventory.urls')),
    path("notice/", include('notice.urls')),
    path("sfa/", include('sfa.urls')),
    path("public/", include('public.urls')),
    path('article/', include('article.urls')),    #首页文章
    # path('404/', TemplateView.as_view(template_name='404.html'), name='404'),
    path('media/', serve, {'document_root': settings.MEDIA_ROOT}),  # 用户上传文件路径，配置上传文件的访问处理函数

    path('attachment_upload.html', task_view.attachment_upload, name='attachment_upload'),
    path("attachment_download.html", task_view.attachment_download, name="attachment_download"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # 配置media
