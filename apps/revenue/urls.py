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
    path("income", views.income, name="income"),
    path("income/edit", views.income_edit, name="income_edit"),
    path("income/delete", views.income_delete, name="income_delete"),
    path("revenue/attach", views.revenue_attach, name="revenue_attach"),
    path("income/detail", views.income_detail, name="income_detail"),
    path("income/detail/1", views.income_detail_1, name="income_detail_1"),
    path("disbursement", views.disbursement, name="disbursement"),
    path("disbursement/edit", views.disbursement_edit, name="disbursement_edit"),
    path("disbursement/delete", views.disbursement_delete, name="disbursement_delete"),
    path("disbursement/detail", views.disbursement_detail, name="disbursement_detail"),
    path("income/classify", views.income_classify, name="income_classify"),
    path("income/classify/edit", views.income_classify_edit, name="income_classify_edit"),
    path("income/classify/delete", views.income_classify_delete, name="income_classify_delete"),
]
