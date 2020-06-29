from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login as do_login
from django.contrib.auth.forms import UserCreationForm
from .models import  Profile, Level, Exercise, Score
from .forms import UCFWithOthers


def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'registration/login.html')

def register(request):
    if request.method == 'POST':
        form = UCFWithOthers(request.POST)
        if form.is_valid():
            us = form.save()
            if us is not None:
                do_login(request, us)
                return redirect('/')
    else:
        form = UCFWithOthers()
    form.fields['username'].help_text = None
    form.fields['password1'].help_text = None
    return render(request, 'registration/register.html', {
        'form':form
    })