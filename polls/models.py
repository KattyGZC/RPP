from datetime import date
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField('Fecha de nacimiento', default=date.today)
    photo = models.ImageField('Foto de perfil', upload_to='media/',
                              max_length=200, default='media/default.png')

    def __str__(self):
        return str(self.user)

class Level(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Exercise(models.Model):
    idLevel = models.ForeignKey(Level, on_delete=models.CASCADE)
    text = models.TextField()
    punctuation = models.IntegerField()

    def __str__(self):
        return self.text

class Score(models.Model):
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)
    idExercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    value = models.FloatField()

