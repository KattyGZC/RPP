import logging
import os

from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from apps.exercises.services import ProgressService
from core.exceptions import BusinessLogicError, ResourceNotFoundError
from core.responses import created_response, error_response

from .services import EvaluationOrchestrator

logger = logging.getLogger(__name__)
_orchestrator = EvaluationOrchestrator()
_progress_service = ProgressService()


class EvaluateReadingView(APIView):
    """
    POST /api/evaluation/evaluate/

    Accepts a multipart request with:
      - audio: audio file (webm/wav/mp4)
      - exercise_id: ID of the exercise being evaluated
      - duration_seconds: how long the recording was (optional)
    """

    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        audio_file = request.FILES.get("audio")
        exercise_id = request.data.get("exercise_id")
        duration_seconds = int(request.data.get("duration_seconds", 0))

        if not audio_file:
            return error_response("El archivo de audio es requerido.", code="MISSING_AUDIO")

        if not exercise_id:
            return error_response("El ID del ejercicio es requerido.", code="MISSING_EXERCISE_ID")

        # Fetch exercise to get expected text
        from apps.exercises.repositories import ExerciseRepository
        exercise = ExerciseRepository().get_by_id(int(exercise_id))
        if not exercise:
            return error_response("Ejercicio no encontrado.", code="NOT_FOUND")

        tmp_path = None
        try:
            tmp_path = _orchestrator.save_audio_temporarily(audio_file)
            result = _orchestrator.evaluate_reading(
                audio_file_path=tmp_path,
                expected_text=exercise.text,
                max_score=exercise.max_score,
            )

            # Persist the reading session
            session = _progress_service.save_reading_session(
                user=request.user,
                exercise_id=exercise.id,
                score=result["score"],
                accuracy=result["accuracy"],
                transcription=result["transcription"],
                feedback=result["feedback"],
                duration_seconds=duration_seconds,
            )

            return created_response(
                data={**result, "session_id": session.id},
                message="Evaluación completada.",
            )

        except (ResourceNotFoundError, BusinessLogicError) as e:
            return error_response(str(e), code=getattr(e, "code", "ERROR"))
        except Exception as e:
            logger.exception("Unexpected error during evaluation: %s", str(e))
            return error_response(
                "Error interno durante la evaluación. Por favor intenta de nuevo.",
                code="EVALUATION_ERROR",
            )
        finally:
            if tmp_path and os.path.exists(tmp_path):
                os.unlink(tmp_path)
