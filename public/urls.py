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
from django.urls import path,include
from . import views


urlpatterns = [
    path("province_city", views.province_city, name='province_city'),
    path("country_town", views.country_town, name='country_town'),
    path("town", views.town_list, name="town_list"),
    path("town_edit", views.town_edit, name='town_edit'),
    path("country", views.country_list, name="country_list"),
    path("country_edit", views.country_edit, name='country_edit'),
    path("city", views.city_list, name="city_list"),
    path("city_edit", views.city_edit, name='city_edit'),
    path("city_country", views.city_country, name="city_country"),
    path("nation", views.nation_list, name="nation_list"),
    path("nation_edit", views.nation_edit, name='nation_edit'),
    path("province", views.province_list, name='province_list'),
    path("province_edit", views.province_edit, name='province_edit'),
]
