from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    #path('/index', views.index, name='index'),
    path('edit/', login_required(views.editProfile), name='edit_profile'),
    path('perfil/', login_required(views.perfil), name='perfil'),
    path('niveles/', login_required(views.choice_level), name='niveles'),
]
