from django.db import models

# Create your models here.

class Role(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class User(models.Model):
    idRol = models.ForeignKey(Role, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    nickname = models.CharField(max_length=50)
    password = models.CharField(max_length=80)
    age = models.IntegerField()
    photo = models.TextField()

    def __str__(self):
        return self.name

class Level(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Exercise(models.Model):
    idLevel = models.ForeignKey(Level, on_delete=models.CASCADE)
    text = models.TextField()
    punctuation = models.IntegerField()


class Score(models.Model):
    idUser = models.ForeignKey(User, on_delete=models.CASCADE)
    idExercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    value = models.FloatField()
    
