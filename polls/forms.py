from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UCFWithOthers(UserCreationForm):
    # Ahora el campo username es de tipo email y cambiamos su texto

    first_name = forms.CharField(label="Nombre")
    last_name = forms.CharField(label='Apellido')

    class Meta:
        model = User
        fields = ["username",'first_name', 'last_name', "password1", "password2"]