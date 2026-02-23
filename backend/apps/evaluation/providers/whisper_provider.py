"""
Local Whisper transcription provider.
Uses faster-whisper (CTranslate2 reimplementation of OpenAI Whisper).
No API key or internet connection required after the model is downloaded.
"""
import logging
import math

from .base import BaseTranscriptionProvider, TranscriptionResult

logger = logging.getLogger(__name__)


class WhisperLocalProvider(BaseTranscriptionProvider):
    """
    Wraps the faster-whisper library.
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
            from faster_whisper import WhisperModel
            logger.info("Loading Whisper model '%s'...", self._model_size)
            self._model = WhisperModel(self._model_size, device="cpu", compute_type="int8")
            logger.info("Whisper model loaded successfully.")
        return self._model

    def transcribe(self, audio_file_path: str, language: str = "es") -> TranscriptionResult:
        logger.debug("Transcribing with Whisper: %s", audio_file_path)
        segments_generator, info = self._loaded_model.transcribe(
            audio_file_path,
            language=language,
            task="transcribe",
        )
        segments = list(segments_generator)
        text = " ".join(s.text.strip() for s in segments)
        return TranscriptionResult(
            text=text.strip(),
            language=language,
            confidence=self._calculate_confidence(segments),
            duration_seconds=info.duration,
        )

    def _calculate_confidence(self, segments: list) -> float:
        if not segments:
            return 0.0
        avg_logprob = sum(s.avg_logprob for s in segments) / len(segments)
        return round(max(0.0, min(1.0, math.exp(avg_logprob))), 3)
