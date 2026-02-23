"""Repository layer for exercises and reading sessions."""
import logging
from typing import Optional

from django.contrib.auth.models import User
from django.db.models import Avg, Count, Max, QuerySet, Sum

from .models import Exercise, Level, ReadingSession

logger = logging.getLogger(__name__)


class LevelRepository:
    def get_all(self) -> QuerySet:
        return Level.objects.annotate(exercise_count=Count("exercises", filter__exercises__is_active=True))

    def get_by_slug(self, slug: str) -> Optional[Level]:
        return Level.objects.filter(slug=slug).first()

    def get_by_id(self, level_id: int) -> Optional[Level]:
        return Level.objects.filter(id=level_id).first()


class ExerciseRepository:
    def get_by_level(self, level: Level) -> QuerySet:
        return Exercise.objects.filter(level=level, is_active=True).select_related("level")

    def get_by_id(self, exercise_id: int) -> Optional[Exercise]:
        return Exercise.objects.filter(id=exercise_id, is_active=True).select_related("level").first()

    def create(self, **kwargs) -> Exercise:
        return Exercise.objects.create(**kwargs)

    def update(self, exercise: Exercise, **kwargs) -> Exercise:
        for field, value in kwargs.items():
            setattr(exercise, field, value)
        exercise.save()
        return exercise

    def delete(self, exercise: Exercise) -> None:
        exercise.is_active = False
        exercise.save(update_fields=["is_active"])


class ReadingSessionRepository:
    def create(self, user: User, exercise: Exercise, score: float, accuracy: float,
               transcription: str, feedback: dict, duration_seconds: int) -> ReadingSession:
        return ReadingSession.objects.create(
            user=user,
            exercise=exercise,
            score=score,
            accuracy=accuracy,
            transcription=transcription,
            feedback=feedback,
            duration_seconds=duration_seconds,
        )

    def get_by_user(self, user: User, limit: int = 20) -> QuerySet:
        return (
            ReadingSession.objects.filter(user=user)
            .select_related("exercise__level")
            .order_by("-created_at")[:limit]
        )

    def get_user_stats_by_level(self, user: User) -> QuerySet:
        """Returns aggregated stats grouped by level for dashboard charts."""
        return (
            ReadingSession.objects.filter(user=user)
            .values("exercise__level__name", "exercise__level__difficulty", "exercise__level__slug")
            .annotate(
                total_sessions=Count("id"),
                avg_score=Avg("score"),
                avg_accuracy=Avg("accuracy"),
                best_score=Max("score"),
                total_score=Sum("score"),
            )
            .order_by("exercise__level__order")
        )

    def get_best_score_for_exercise(self, user: User, exercise: Exercise) -> Optional[float]:
        result = ReadingSession.objects.filter(user=user, exercise=exercise).aggregate(best=Max("score"))
        return result["best"]

    def get_student_summary(self, user: User) -> dict:
        """Summary used in teacher's student progress view."""
        stats = ReadingSession.objects.filter(user=user).aggregate(
            total_sessions=Count("id"),
            avg_score=Avg("score"),
            avg_accuracy=Avg("accuracy"),
        )
        return stats
