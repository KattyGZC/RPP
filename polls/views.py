from django.shortcuts import render, redirect
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
    # Suma puntajes nivel básico
    score_1 = scores_list(1, request.user)

    # Suma puntajes nivel intermedio
    score_2 = scores_list(2, request.user)

    # Suma puntajes nivel avanzado
    score_3 = scores_list(3, request.user)

    context = {
        'score_1': score_1,
        'score_2': score_2,
        'score_3': score_3,
    }
    return render(request, 'perfil.html', context)

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
    score_acum = scores_list(level, request.user)
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
    scr = Score.objects.filter(idExercise=request.POST['idExercise'], idUser=request.user)
    exer = Exercise.objects.get(id=request.POST['idExercise'])
    print(exer.idLevel_id)
    if request.method == 'POST' and request.is_ajax():
        if scr:
            scr.update(value=request.POST['value'])
        else:
            scr = Score(idUser=request.user, idExercise=exer, value=request.POST['value'])
            scr.save()
        total_score = scores_list(exer.idLevel_id, request.user)
    return HttpResponse(total_score, 'application/javascript')

def scores_list(level, id_user):
    obj_exercise1 = Exercise.objects.filter(idLevel=level)
    list_scores_1 = []
    for item in obj_exercise1:
        obj_score = Score.objects.filter(idExercise=item.id, idUser=id_user)
        for v in obj_score:
            list_scores_1.append(round(float(v.value), 2))
    sum_scores = sum(list_scores_1)
    return sum_scores
    