from django.http import HttpResponse
from django.shortcuts import render
from .models import  Profile, Level, Exercise, Score


def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'registration/login.html')

def register(request):
    return render(request, 'registration/register.html')