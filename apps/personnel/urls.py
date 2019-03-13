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
from . import views

urlpatterns = [
    path("job_rank", views.job_rank_list, name="job_rank_list"),
    path("job_rank/edit", views.job_rank_edit, name='job_rank_edit'),
    path("job_title", views.job_title_list, name="job_title_list"),
    path("job_title/edit", views.job_title_edit, name='job_title_edit'),
    path("project", views.project_list, name="project_list"),
    path("project/edit", views.project_edit, name='project_edit'),
    path("company", views.company_list, name="company_list"),
    path("company/edit", views.company_edit, name='company_edit'),
    path("department",views.department_list, name="department_list"),
    path("department/edit",views.department_edit, name='department_edit'),
    path("staff", views.staff_list, name="staff_list"),
    path("staff/edit", views.staff_edit, name='staff_edit'),

    path("staff/edit1", views.staff_edit1, name='staff_edit1'),
    path("staff/edit2", views.staff_edit2, name='staff_edit2'),
    path("staff/edit3", views.staff_edit3, name='staff_edit3'),
    path("staff/edit4", views.staff_edit4, name='staff_edit4'),
    path("staff/edit5", views.staff_edit5, name='staff_edit5'),

    path("staff/detail1", views.staff_detail_1, name='staff_detail_1'),
    path("staff/detail2", views.staff_detail_2, name='staff_detail_2'),
    path("staff/detail3", views.staff_detail_3, name='staff_detail_3'),
    path("staff/detail4", views.staff_detail_4, name='staff_detail_4'),
    path("staff/detail5", views.staff_detail_5, name='staff_detail_5'),

    path("staff/delete1", views.staff_delete1, name='staff_dalete1'),
    path("staff/delete2", views.staff_delete2, name='staff_dalete2'),
    path("staff/delete3", views.staff_delete3, name='staff_dalete3'),
    path("staff/delete4", views.staff_delete4, name='staff_dalete4'),
    path("staff/delete5", views.staff_delete5, name='staff_dalete5'),

    path("staff/detail", views.staff_detail, name='staff_detail'),

    # path("staff/detail",views.staff_detail,name="staff_detail"),
    path("staff/delete",views.staff_delete,name="staff_delete"),
    path("staff_select", views.staff_select, name='staff_select'),
    path("upload_life_photo", views.life_photo, name="life_photo"),
    path("upload_attach", views.staff_attach, name="staff_attach"),

    #  new
    #  setting delete
    path("company/delete",views.company_delete,name="company_delete"),
    path("department/delete", views.department_delete, name="department_delete"),
    path("project/delete", views.project_delete, name="project_delete"),
    path("job_rank/delete", views.job_rank_delete, name="job_rank_delete"),
    path("job_title/delete", views.job_title_delete, name="job_title_delete")

]
