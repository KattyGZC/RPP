import logging

from django.contrib.auth.models import User
from django.db import models

logger = logging.getLogger(__name__)


class DifficultyLevel(models.TextChoices):
    BASIC = "basic", "Básico"
    INTERMEDIATE = "intermediate", "Intermedio"
    ADVANCED = "advanced", "Avanzado"


class Level(models.Model):
    """Groups exercises by difficulty."""

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    difficulty = models.CharField(max_length=20, choices=DifficultyLevel.choices)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to="levels/", null=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Nivel"
        verbose_name_plural = "Niveles"

    def __str__(self):
        return self.name

    @property
    def exercise_count(self) -> int:
        return self.exercises.filter(is_active=True).count()


class Exercise(models.Model):
    """A reading text that students must read aloud."""

    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name="exercises")
    title = models.CharField(max_length=200)
    text = models.TextField()
    max_score = models.FloatField(default=100.0)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_exercises",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "created_at"]
        verbose_name = "Ejercicio"
        verbose_name_plural = "Ejercicios"

    def __str__(self):
        return f"[{self.level.name}] {self.title}"


class ReadingSession(models.Model):
    """
    Records a single reading attempt with full AI evaluation results.
    Separating sessions from scores allows full history and analytics.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reading_sessions")
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name="sessions")
    score = models.FloatField()
    accuracy = models.FloatField()
    transcription = models.TextField(blank=True)
    feedback = models.JSONField(default=dict)
    duration_seconds = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Sesión de Lectura"
        verbose_name_plural = "Sesiones de Lectura"

    def __str__(self):
        return f"{self.user.username} — {self.exercise.title} ({self.score:.1f}pts)"
