from django.urls import path
from . import views

urlpatterns = [
    path('', views.merchants_home, name='merchants_home'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
]
