from django.contrib import admin

from .models import Role, User, Level, Exercise, Score

admin.site.register(Role)
admin.site.register(User)
admin.site.register(Level)
admin.site.register(Exercise)
admin.site.register(Score)

