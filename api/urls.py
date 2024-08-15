from django.urls import path
from . import views


urlpatterns = [
    path('', views.main),
    path('create-pay', views.create_pay)
]
