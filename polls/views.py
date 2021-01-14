from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login as do_login
from django.contrib.auth.models import User
from django.core import serializers
from .models import Exercise, Score
from .forms import UCFWithOthers, UEditF, ProfileForm, ScoreForm

def error_404_view(request):
    return render(request, '404.html')

def index(request):
    list_user = User.objects.all()
    list_scores = []
    list_score_user_level1 = []
    list_score_user_level2 = []
    list_score_user_level3 = []
    for level in range(1, 4):
        obj_exercise = Exercise.objects.filter(idLevel=level)
        sum_scores = 0
        for id_user in list_user:
            for item in obj_exercise:
                obj_score = Score.objects.filter(idExercise=item.id, idUser=id_user.id)
                for v in obj_score:
                    list_scores.append(round(float(v.value), 2))
                sum_scores = sum(list_scores)
            list_scores = []
            print(level)
            if level == 1:    
                list_score_user_level1.append([sum_scores, id_user.username])
            elif level == 2:
                list_score_user_level2.append([sum_scores, id_user.username])
            else:
                list_score_user_level3.append([sum_scores, id_user.username])
            sum_scores = 0
    list_score_user_level1 = sorted(list_score_user_level1, reverse=True)
    list_score_user_level2 = sorted(list_score_user_level2, reverse=True)
    list_score_user_level3 = sorted(list_score_user_level3, reverse=True)
    level1 = list_score_user_level1[:5]
    level2 = list_score_user_level2[:5]
    level3 = list_score_user_level3[:5]

    cont = 1
    for l in level1:
        l.append(cont)
        cont+=1
    cont = 1
    for l in level2:
        l.append(cont)
        cont+=1
    cont = 1
    for l in level3:
        l.append(cont)
        cont+=1
        
    context= {
        'list_score_user_level1': level1,
        'list_score_user_level2': level2,
        'list_score_user_level3': level3,
    }
    return render(request, 'index.html', context)

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
    form.fields['password1'].help_text = """• Su contraseña no puede tener parecido con el resto de su información personal.\n
                                            • Su contraseña debe contener al menos 8 caracteres.\n
                                            • Su contraseña no puede ser completamente numérica."""
    form.fields['password2'].help_text = 'Para verificar introduzca la misma contraseña que colocó en el campo anterior.'
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
    level = None
    if request.method == "POST":
        for key, value in request.POST.items():
            if key == 'level':
                level = value
    if level:       
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
    else:
        return redirect('/')

def save_exercise(request):
    scr = Score.objects.filter(idExercise=request.POST['idExercise'], idUser=request.user)
    exer = Exercise.objects.get(id=request.POST['idExercise'])
    if request.method == 'POST' and request.is_ajax():
        if scr:
            scr.update(value=request.POST['value'])
        else:
            scr = Score(idUser=request.user, idExercise=exer, value=request.POST['value'])
            scr.save()
        total_score = scores_list(exer.idLevel_id, request.user)
    return HttpResponse(total_score, 'application/javascript')

def scores_list(level, id_user):
    obj_exercise = Exercise.objects.filter(idLevel=level)
    list_scores = []
    for item in obj_exercise:
        obj_score = Score.objects.filter(idExercise=item.id, idUser=id_user)
        for v in obj_score:
            list_scores.append(round(float(v.value), 2))
    sum_scores = sum(list_scores)
    return sum_scores
    