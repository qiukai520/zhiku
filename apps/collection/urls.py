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
    path("collect", views.collect, name="collect"),
    path("collections", views.collections, name="collections"),
    path("collect/delete",views.collect_delete,name="collect_delete"),
    path("knowledges", views.knowledge, name="knowledges"),
    path("knowledge/detail",views.knowledge_detail, name="knowledge_detail"),
    path("knowledge/favor", views.knowledge_favor, name="knowledge_favor"),

]
