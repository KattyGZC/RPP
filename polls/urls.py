from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path('/index', views.index, name='index'),
    path('/login', views.login, name='login'),
]
