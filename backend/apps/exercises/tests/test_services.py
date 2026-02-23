from django.contrib.auth.models import User
from django.test import TestCase

from apps.exercises.models import DifficultyLevel, Exercise, Level
from apps.exercises.services import ExerciseService, ProgressService
from core.exceptions import BusinessLogicError, ResourceNotFoundError


class ExerciseServiceTests(TestCase):
    def setUp(self):
        self.service = ExerciseService()
        self.teacher = User.objects.create_user(
            username="teacher", password="pass123", first_name="Profe", last_name="García"
        )
        self.teacher.profile.role = "teacher"
        self.teacher.profile.save()

        self.level = Level.objects.create(
            name="Básico", slug="basico", difficulty=DifficultyLevel.BASIC, order=1
        )

    def test_create_exercise(self):
        exercise = self.service.create_exercise(
            teacher=self.teacher,
            level_id=self.level.id,
            title="Mi primer texto",
            text="El sol sale por el oriente.",
            max_score=100.0,
        )
        self.assertIsInstance(exercise, Exercise)
        self.assertEqual(exercise.title, "Mi primer texto")
        self.assertEqual(exercise.created_by, self.teacher)

    def test_create_exercise_invalid_level(self):
        with self.assertRaises(ResourceNotFoundError):
            self.service.create_exercise(
                teacher=self.teacher,
                level_id=9999,
                title="Test",
                text="Some text",
            )

    def test_delete_exercise_soft_deletes(self):
        exercise = self.service.create_exercise(
            teacher=self.teacher, level_id=self.level.id,
            title="Delete me", text="Some text"
        )
        self.service.delete_exercise(exercise.id)
        exercise.refresh_from_db()
        self.assertFalse(exercise.is_active)


class ProgressServiceTests(TestCase):
    def setUp(self):
        self.service = ProgressService()
        self.student = User.objects.create_user(username="student", password="pass123")
        self.level = Level.objects.create(
            name="Básico", slug="basico", difficulty=DifficultyLevel.BASIC, order=1
        )
        self.exercise = Exercise.objects.create(
            level=self.level, title="Ejercicio 1", text="El gato y el perro.", max_score=100.0
        )

    def test_save_session_validates_score_range(self):
        with self.assertRaises(BusinessLogicError) as ctx:
            self.service.save_reading_session(
                user=self.student,
                exercise_id=self.exercise.id,
                score=200.0,
                accuracy=80.0,
                transcription="El gato y el perro.",
                feedback={},
                duration_seconds=10,
            )
        self.assertEqual(ctx.exception.code, "SCORE_OUT_OF_RANGE")

    def test_save_session_success(self):
        session = self.service.save_reading_session(
            user=self.student,
            exercise_id=self.exercise.id,
            score=75.0,
            accuracy=82.5,
            transcription="El gato y el perro.",
            feedback={"correct_words": ["gato"], "incorrect_words": []},
            duration_seconds=12,
        )
        self.assertEqual(session.user, self.student)
        self.assertEqual(session.score, 75.0)
