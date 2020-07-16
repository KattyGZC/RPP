from django.urls import path, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    #path('/index', views.index, name='index'),
    path('edit/', login_required(views.edit_profile), name='edit_profile'),
    path('perfil/', login_required(views.perfil), name='perfil'),
    path('niveles/', login_required(views.choice_level), name='niveles'),
    path('ejercicios/', login_required(views.exercises), name='ejercicios')
]
