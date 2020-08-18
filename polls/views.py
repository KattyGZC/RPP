from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login as do_login
from django.core import serializers
from .models import  Profile, Level, Exercise, Score
from .forms import UCFWithOthers, UEditF, ProfileForm, ScoreForm

def error_404_view(request):
    return render(request, '404.html')

def index(request):
    return render(request, 'index.html')

def perfil(request):
    return render(request, 'perfil.html')

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

def edit_profile(request):
    if request.method == 'POST':
        form = UEditF(request.POST, instance=request.user)
        extended_profile_form = ProfileForm(request.POST, request.FILES,
                                            instance=request.user.profile)
        if form.is_valid() and extended_profile_form.is_valid():
            form.save()
            extended_profile_form.save()
            return redirect('/polls/perfil')
    else:
        form = UEditF(instance=request.user)
        extended_profile_form = ProfileForm(instance=request.user.profile)

    context = {
        'form': form,
        'extended_profile_form':extended_profile_form
    }
    form.fields['password'].help_text = 'Para cambiar la contraseña has clic en el menú superior derecho "Cambiar contraseña"'
    return render(request, 'registration/edit_profile.html', context)

def choice_level(request):
    return render(request, 'niveles.html')

def exercises(request):
    if request.method == "POST":
        for key, value in request.POST.items():
            if key == 'level':
                level = value
    obj_exercise = Exercise.objects.filter(idLevel=level)
    exercise_json = serializers.serialize('json', obj_exercise)
    form = ScoreForm()
    context = {
        'level': level,
        'json_exercise': exercise_json,
        'form': form
    }
    return render(request, 'ejercicios.html', context)

def save_exercise(request):
    if request.method == 'POST' and request.is_ajax:
        form_score = ScoreForm(request.POST, instance=request.user)
        if form_score.is_valid():
            print(request.POST.get('value'))
            print(request.POST.get('idUser'))
            print(request.POST.get('idExercise'))
            form_score.save()
        else:
            print('Tenemos un error')
    return HttpResponse('Respuesta')
