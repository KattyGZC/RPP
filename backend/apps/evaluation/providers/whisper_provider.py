"""
Local Whisper transcription provider.
Uses OpenAI's open-source Whisper model running entirely on local hardware.
No API key or internet connection required after the model is downloaded.
"""
import logging
import math

from .base import BaseTranscriptionProvider, TranscriptionResult

logger = logging.getLogger(__name__)


class WhisperLocalProvider(BaseTranscriptionProvider):
    """
    Wraps the openai-whisper library.
    The model is loaded lazily on first use to avoid startup delays.
    Model is cached in memory for subsequent calls.
    """

    def __init__(self, model_size: str = "small"):
        self._model_size = model_size
        self._model = None

    @property
    def provider_name(self) -> str:
        return f"whisper_local:{self._model_size}"

    @property
    def _loaded_model(self):
        """Lazy-load the model on first access (Lazy Initialization pattern)."""
        if self._model is None:
            import whisper
            logger.info("Loading Whisper model '%s'...", self._model_size)
            self._model = whisper.load_model(self._model_size)
            logger.info("Whisper model loaded successfully.")
        return self._model

    def transcribe(self, audio_file_path: str, language: str = "es") -> TranscriptionResult:
        logger.debug("Transcribing with Whisper: %s", audio_file_path)
        result = self._loaded_model.transcribe(
            audio_file_path,
            language=language,
            task="transcribe",
            fp16=False,  # Safer on CPU; set to True only on GPU
        )
        return TranscriptionResult(
            text=result["text"].strip(),
            language=language,
            confidence=self._calculate_confidence(result),
            duration_seconds=result.get("duration", 0.0),
        )

    def _calculate_confidence(self, result: dict) -> float:
        segments = result.get("segments", [])
        if not segments:
            return 0.0
        avg_logprob = sum(s.get("avg_logprob", -1.0) for s in segments) / len(segments)
        return round(max(0.0, min(1.0, math.exp(avg_logprob))), 3)
