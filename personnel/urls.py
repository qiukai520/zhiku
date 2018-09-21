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
    path("job_rank_edit", views.job_rank_edit, name='job_rank_edit'),
    path("job_title", views.job_title_list, name="job_title_list"),
    path("job_title_edit", views.job_title_edit, name='job_title_edit'),
    path("project", views.project_list, name="project_list"),
    path("project_edit", views.project_edit, name='project_edit'),
    path("company", views.company_list, name="company_list"),
    path("company_edit", views.company_edit, name='company_edit'),
    path("department",views.department_list, name="department_list"),
    path("department_edit",views.department_edit, name='department_edit'),
    path("staff", views.staff_list, name="staff_list"),
    path("staff_edit", views.staff_edit, name='staff_edit'),
    path("staff_detail",views.staff_detail,name="staff_detail"),
    path("staff_delete",views.staff_delete,name="staff_delete"),
    path("upload_life_photo", views.life_photo, name="life_photo"),
    path("upload_attach", views.staff_attach, name="staff_attach"),

]
