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
    path("period/detail",views.task_period_detail,name="task_period_detail"),
    path('delete', views.task_delete, name="task_delete"),
    path('map/delete', views.task_map_delete, name="task_map_delete"),
    path('period/delete', views.task_period_delete, name="task_period_delete"),
    path('map/cancel', views.task_map_cancel, name="task_map_cancel"),
    path('period/cancel', views.task_period_cancel, name="task_period_cancel"),
    path("base_detail", views.task_base_detail, name="task_base_detail"),
    path('assign/center', views.task_assign_center, name='task_assign_center'),
    path('map/edit', views.task_map_edit, name="task_map_edit"),
    path('map/content', views.task_map_content, name="map_content"),
    #task_period
    path('period', views.task_period, name="task_period"),
    # path("task_team_assign.html", views.task_team_assign, name="task_team_assign"),
    path("assign", views.task_assign, name="task_assign"),
    path('assigned', views.task_assign_list, name="task_assign_list"),
    path('assign/edit', views.task_assign_edit, name="task_assign_edit"),
    path('assign/content', views.show_assign_content, name="show_assign_content"),
    # path('task_mutil_assign.html', views.task_mutil_assign, name="task_mutil_assign"),
    path('review/center', views.task_wait_review, name="task_wait_review"),
    path("review", views.task_review, name='task_review'),
    path("review/record",views.task_review_record,name="task_review_record.html"),
    path('personal/review', views.personal_task_review, name='personal_task_review'),
    path('personal', views.personal_task_list, name='personal_task_list'),
    path('personal/detail', views.personal_task_detail, name='personal_task_detail'),
    path('complete', views.complete_task, name='complete_task'),
    path('sort/edit', views.task_sort_edit, name="task_sort_edit"),
    path('sorts', views.task_sort_list, name='task_sort_list'),
    path('sort/delete', views.task_sort_delete, name="task_sort_delete"),
    path('perfors', views.performence_display, name='performence_list'),
    path('perfor/edit', views.performence_edit, name="performence_edit"),
    path('perfor/statistic', views.performence_statistic, name="performence_statistic"),
    path("perfor/statistic/detail",views.perfor_statistic_detail,name="perfor_statistic_detail"),
    path('perfor/delete',views.performence_delete, name="performence_delete"),
    path('department/staff', views.department_staff, name="department_staff"),

]
