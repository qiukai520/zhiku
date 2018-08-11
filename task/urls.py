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

    path('add', views.publish_task, name="publish_task"),
    path('edit', views.task_edit, name='task_edit'),
    path("detail", views.task_detail, name="task_detail"),
    path('delete', views.task_delete, name="task_delete"),
    path("base_detail", views.task_base_detail, name="task_base_detail"),
    path('assign_center', views.task_assign_center, name='task_assign_center'),
    path('map_edit', views.task_map_edit, name="task_map_edit"),
        # path("task_team_assign.html", views.task_team_assign, name="task_team_assign"),
    path("assign", views.task_assign, name="task_assign"),
    path('assigned_list', views.task_assign_list, name="task_assign_list"),
    path('assign_edit', views.task_assign_edit, name="task_assign_edit"),
    path('assign_content', views.show_assign_content, name="show_assign_content"),
    # path('task_mutil_assign.html', views.task_mutil_assign, name="task_mutil_assign"),
    path('wait_review', views.task_wait_review, name="task_wait_review"),
    path("review", views.task_review, name='task_review'),
    path("review_record",views.task_review_record,name="task_review_record.html"),
    path('personal_review', views.personal_task_review, name='personal_task_review'),
    path('personal_list', views.personal_task_list, name='personal_task_list'),
    path('personal_detail', views.personal_task_detail, name='personal_task_detail'),
    path('complete', views.complete_task, name='complete_task'),
    path('sort_edit', views.task_sort_edit, name="task_sort_edit"),
    path('sort_list', views.task_sort_list, name='task_sort_list'),
    path('sort_delete', views.task_sort_delete, name="task_sort_delete"),
    path('performence_list', views.performence_display, name='performence_list'),
    path('performence_edit', views.performence_edit, name="performence_edit"),
    path('performence_statistic', views.performence_statistic, name="performence_statistic"),
    path("perfor_statistic_detail",views.perfor_statistic_detail,name="perfor_statistic_detail"),
    path('performence_delete',views.performence_delete, name="performence_delete"),
    path('department_staff', views.department_staff, name="department_staff"),

]
