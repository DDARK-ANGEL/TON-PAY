from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('pay', views.pay),
    path('check', views.check),
    path('check-info', views.check_info),
    path('create-pay', views.create_pay)
]
