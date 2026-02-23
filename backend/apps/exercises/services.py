"""Business logic for exercises and progress tracking."""
import logging

from django.contrib.auth.models import User

from core.exceptions import BusinessLogicError, ResourceNotFoundError

from .models import Exercise, Level
from .repositories import ExerciseRepository, LevelRepository, ReadingSessionRepository

logger = logging.getLogger(__name__)

_level_repo = LevelRepository()
_exercise_repo = ExerciseRepository()
_session_repo = ReadingSessionRepository()


class ExerciseService:
    """Manages exercise and level CRUD (teacher-facing operations)."""

    def get_all_levels(self):
        return _level_repo.get_all()

    def get_exercises_for_level(self, level_slug: str):
        level = _level_repo.get_by_slug(level_slug)
        if not level:
            raise ResourceNotFoundError("Level", level_slug)
        return _exercise_repo.get_by_level(level)

    def create_exercise(self, teacher: User, level_id: int, title: str, text: str,
                        max_score: float = 100.0, order: int = 0) -> Exercise:
        level = _level_repo.get_by_id(level_id)
        if not level:
            raise ResourceNotFoundError("Level", level_id)

        return _exercise_repo.create(
            level=level,
            title=title,
            text=text,
            max_score=max_score,
            order=order,
            created_by=teacher,
        )

    def update_exercise(self, exercise_id: int, **kwargs) -> Exercise:
        exercise = _exercise_repo.get_by_id(exercise_id)
        if not exercise:
            raise ResourceNotFoundError("Exercise", exercise_id)
        return _exercise_repo.update(exercise, **kwargs)

    def delete_exercise(self, exercise_id: int) -> None:
        exercise = _exercise_repo.get_by_id(exercise_id)
        if not exercise:
            raise ResourceNotFoundError("Exercise", exercise_id)
        _exercise_repo.delete(exercise)


class ProgressService:
    """Calculates and aggregates student progress data."""

    def get_user_progress(self, user: User) -> dict:
        """Full dashboard data for a student."""
        stats_by_level = list(_session_repo.get_user_stats_by_level(user))
        recent_sessions = list(_session_repo.get_by_user(user, limit=10))

        return {
            "stats_by_level": stats_by_level,
            "recent_sessions": recent_sessions,
        }

    def get_student_summary_for_teacher(self, student: User) -> dict:
        """Quick stats for teacher dashboard."""
        return _session_repo.get_student_summary(student)

    def save_reading_session(self, user: User, exercise_id: int, score: float,
                             accuracy: float, transcription: str,
                             feedback: dict, duration_seconds: int):
        exercise = _exercise_repo.get_by_id(exercise_id)
        if not exercise:
            raise ResourceNotFoundError("Exercise", exercise_id)

        if not (0 <= score <= exercise.max_score):
            raise BusinessLogicError(
                f"El puntaje {score} está fuera del rango permitido [0, {exercise.max_score}].",
                code="SCORE_OUT_OF_RANGE",
            )

        return _session_repo.create(
            user=user,
            exercise=exercise,
            score=score,
            accuracy=accuracy,
            transcription=transcription,
            feedback=feedback,
            duration_seconds=duration_seconds,
        )
