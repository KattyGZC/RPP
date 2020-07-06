from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    #path('/index', views.index, name='index'),
    path('edit/', login_required(views.editProfile), name='edit_profile'),
    
]
