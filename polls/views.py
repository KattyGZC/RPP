from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import login as do_login
from django.core import serializers
from .models import Exercise, Score
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
    list_scores = []
    for item in obj_exercise:
        obj_score = Score.objects.filter(idExercise=item.id, idUser=request.user)
        for v in obj_score:
            list_scores.append(float(v.value))
    score_acum = sum(list_scores)
    exercise_json = serializers.serialize('json', obj_exercise)
    form = ScoreForm()
    context = {
        'score_acum': score_acum,
        'level': level,
        'json_exercise': exercise_json,
        'form': form
    }
    return render(request, 'ejercicios.html', context)

def save_exercise(request):
    if request.method == 'POST' and request.is_ajax():
        exer = Exercise.objects.get(id=request.POST['idExercise'])
        scr = Score(idUser=request.user, idExercise=exer, value=request.POST['value'])
        scr.save()
    return HttpResponse('Respuesta')
