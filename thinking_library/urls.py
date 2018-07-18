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
from task import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('xadmin/', xadmin.site.urls),
    path('index/', views.index, name='index'),
    path('task_publish.html', views.publish_task, name="publish_task"),
    path('attachment_upload.html', views.attachment_upload, name='attachment_upload'),
    path("attachment_download.html",views.attachment_download, name="attachment_download"),
    path('task_assign_center.html', views.task_assign_center, name='task_assign_center'),
    path('task_edit.html', views.task_edit, name='task_edit'),
    path('task_delete_html', views.task_delete, name="task_delete"),
    path("task_detail.html", views.task_detail, name="task_detail"),
    # path("task_team_assign.html", views.task_team_assign, name="task_team_assign"),
    path("task_assign.html", views.task_assign, name="task_assign"),
    path('task_assigned_list.html', views.task_assign_list, name="task_assign_list"),
    path('task_assign_edit.html', views.task_assign_edit, name="task_assign_edit"),
    # path('task_mutil_assign.html', views.task_mutil_assign, name="task_mutil_assign"),
    path('task_wait_review.html', views.task_wait_review, name="task_wait_review"),
    path("task_review.html", views.task_review, name='task_review'),
    path("task_review_record.html",views.task_review_record,name="task_review_record.html"),
    path('task_sort_edit.html', views.task_sort_edit, name="task_sort_edit"),
    path('task_sort_list.html', views.task_sort_list, name='task_sort_list'),
    path('task_sort_delete.html', views.task_sort_delete, name="task_sort_delete"),
    path('personal_task_review.html', views.personal_task_review, name='personal_task_review'),
    path('personal_task_list.html', views.personal_task_list, name='personal_task_list'),
    path('complete_task.html', views.complete_task, name='complete_task'),
    path('show_assign_content.html', views.show_assign_content, name="show_assign_content"),
    path('get_department_staff.html', views.department_staff, name="department_staff"),
    path('performence_list.html', views.performence_display, name='performence_list'),
    path('performence_edit.html', views.performence_edit, name="performence_edit"),
    path('performence_delete.html',views.performence_delete, name="performence_delete"),

]
