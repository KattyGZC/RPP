from datetime import date
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Profile

class UCFWithOthers(UserCreationForm):

    first_name = forms.CharField(label="Nombre")
    last_name = forms.CharField(label='Apellido')

    class Meta:
        model = User
        fields = ["username",'first_name', 'last_name', "password1", "password2"]

class UEditF(UserChangeForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name']

class ProfileForm(forms.ModelForm):

    birth_date = forms.DateField(label='Fecha de nacimiento')
    photo = forms.ImageField(label="Foto de perfil")

    class Meta:
        model = Profile
        fields = ['birth_date', 'photo']
