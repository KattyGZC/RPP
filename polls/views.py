from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login as do_login
from django.contrib.auth.forms import PasswordChangeForm
from django.template import RequestContext
from .models import  Profile, Level, Exercise, Score
from .forms import UCFWithOthers, UEditF, ProfileForm

def error_404_view(request, exception):
    return render(request,'404.html')

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

def editProfile(request):
    if request.method == 'POST':
        form = UEditF(request.POST, instance=request.user)
        extended_profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)        
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

# def changePassword(request):
#     form = UserChangePass(request.POST)
#     return render(request, 'registration/password_change.html', {
#         'form': form,
#     })

def choice_level(request):
    return render(request, 'niveles.html')

