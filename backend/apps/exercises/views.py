import logging

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from core.exceptions import BusinessLogicError, ResourceNotFoundError
from core.permissions import IsTeacherOrAdmin
from core.responses import created_response, error_response, no_content_response, success_response

from .serializers import (
    ExerciseCreateSerializer,
    ExerciseSerializer,
    ExerciseUpdateSerializer,
    LevelSerializer,
    LevelStatsSerializer,
    ReadingSessionSerializer,
)
from .services import ExerciseService, ProgressService

logger = logging.getLogger(__name__)
_exercise_service = ExerciseService()
_progress_service = ProgressService()


class LevelListView(APIView):
    """GET /api/exercises/levels/"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        levels = _exercise_service.get_all_levels()
        return success_response(data=LevelSerializer(levels, many=True).data)


class ExerciseListView(APIView):
    """
    GET  /api/exercises/?level=<slug>   List exercises for a level
    POST /api/exercises/                Create exercise (teachers only)
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        level_slug = request.query_params.get("level")
        if not level_slug:
            return error_response("El parámetro 'level' es requerido.", code="MISSING_PARAM")
        try:
            exercises = _exercise_service.get_exercises_for_level(level_slug)
            return success_response(data=ExerciseSerializer(exercises, many=True).data)
        except ResourceNotFoundError as e:
            return error_response(str(e), code="NOT_FOUND", status_code=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        if not request.user.profile.is_teacher:
            return error_response("Solo los profesores pueden crear ejercicios.", code="FORBIDDEN",
                                  status_code=status.HTTP_403_FORBIDDEN)
        serializer = ExerciseCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response("Datos inválidos.", code="VALIDATION_ERROR")
        try:
            exercise = _exercise_service.create_exercise(teacher=request.user, **serializer.validated_data)
            return created_response(data=ExerciseSerializer(exercise).data, message="Ejercicio creado.")
        except ResourceNotFoundError as e:
            return error_response(str(e), code="NOT_FOUND", status_code=status.HTTP_404_NOT_FOUND)


class ExerciseDetailView(APIView):
    """
    PATCH  /api/exercises/<id>/   Update exercise (teachers only)
    DELETE /api/exercises/<id>/   Soft-delete exercise (teachers only)
    """

    permission_classes = [IsAuthenticated, IsTeacherOrAdmin]

    def patch(self, request, exercise_id: int):
        serializer = ExerciseUpdateSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response("Datos inválidos.", code="VALIDATION_ERROR")
        try:
            exercise = _exercise_service.update_exercise(exercise_id, **serializer.validated_data)
            return success_response(data=ExerciseSerializer(exercise).data)
        except ResourceNotFoundError as e:
            return error_response(str(e), code="NOT_FOUND", status_code=status.HTTP_404_NOT_FOUND)

    def delete(self, request, exercise_id: int):
        try:
            _exercise_service.delete_exercise(exercise_id)
            return no_content_response()
        except ResourceNotFoundError as e:
            return error_response(str(e), code="NOT_FOUND", status_code=status.HTTP_404_NOT_FOUND)


class UserProgressView(APIView):
    """GET /api/exercises/progress/ — Student's own dashboard data"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        progress = _progress_service.get_user_progress(request.user)
        return success_response(
            data={
                "stats_by_level": LevelStatsSerializer(progress["stats_by_level"], many=True).data,
                "recent_sessions": ReadingSessionSerializer(progress["recent_sessions"], many=True).data,
            }
        )


class StudentProgressView(APIView):
    """GET /api/exercises/progress/<user_id>/ — Specific student's data (teacher only)"""

    permission_classes = [IsAuthenticated, IsTeacherOrAdmin]

    def get(self, request, user_id: int):
        from django.contrib.auth.models import User
        try:
            student = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return error_response("Estudiante no encontrado.", code="NOT_FOUND",
                                  status_code=status.HTTP_404_NOT_FOUND)

        progress = _progress_service.get_user_progress(student)
        return success_response(
            data={
                "student": {"id": student.id, "username": student.username,
                            "full_name": student.get_full_name()},
                "stats_by_level": LevelStatsSerializer(progress["stats_by_level"], many=True).data,
                "recent_sessions": ReadingSessionSerializer(progress["recent_sessions"], many=True).data,
            }
        )
