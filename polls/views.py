from django.http import HttpResponse
from django.shortcuts import render
from .models import  Profile, Level, Exercise, Score


# def index(request):
#     #return HttpResponse("Hello, world. You're at the polls index.")
#     return render(request, 'index.html')

def signin(request):
    return render(request, 'sign_in.html')