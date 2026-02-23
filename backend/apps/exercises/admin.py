from django.contrib import admin

from .models import Exercise, Level, ReadingSession


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ["name", "difficulty", "order", "exercise_count"]
    prepopulated_fields = {"slug": ("name",)}
    ordering = ["order"]

    @admin.display(description="Ejercicios activos")
    def exercise_count(self, obj):
        return obj.exercises.filter(is_active=True).count()


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ["title", "level", "max_score", "order", "is_active", "created_at"]
    list_filter = ["level", "is_active"]
    search_fields = ["title", "text"]
    ordering = ["level__order", "order"]


@admin.register(ReadingSession)
class ReadingSessionAdmin(admin.ModelAdmin):
    list_display = ["user", "exercise", "score", "accuracy", "duration_seconds", "created_at"]
    list_filter = ["exercise__level"]
    search_fields = ["user__username", "exercise__title"]
    readonly_fields = ["transcription", "feedback"]
