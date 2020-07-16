from django.contrib import admin
from .models import Profile, User, Level, Exercise, Score


admin.site.register(Level)
admin.site.register(Score)

class ProfileAdmin(admin.ModelAdmin):

    list_display = ('user', 'birth_date')

class ExerciseAdmin(admin.ModelAdmin):
    
    list_display = ('text', 'punctuation', 'idLevel')

admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Profile, ProfileAdmin)
