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

from django.urls import path
from . import views

urlpatterns = [
    path("assigned", views.service_assign, name="service_assign"),
    path("my_assign",views.my_assign, name="my_assign"),
    path("contract_follow", views.contract_follow, name="contract_follow"),
    path("ways", views.way_list, name="ways"),
    path("way_edit", views.way_edit, name="way_edit"),
    path("contacts", views.contact_list, name="contacts"),
    path("contact_edit", views.contact_edit, name="contact_edit"),
    path("follow/detail",views.follow_detail,name="crt_follow_detail"),
    path("follow/delete", views.follow_delete, name="crt_follow_delete"),
    # new
    path("follow_way/delete", views.follow_way_delete, name="s_follow_way_delete"),
    path("follow_contact/delete", views.follow_contact_delete, name="s_follow_contact_delete"),

]
