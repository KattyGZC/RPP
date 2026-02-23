"""
OpenAI provider — supports both Whisper API (transcription) and GPT (feedback).
Activated when OPENAI_API_KEY is set and the relevant AI_*_PROVIDER env vars point to "openai".
"""
import logging

from .base import BaseFeedbackProvider, BaseTranscriptionProvider, EvaluationResult, FeedbackResult, TranscriptionResult
from .nlp_provider import NLPFeedbackProvider

logger = logging.getLogger(__name__)


class OpenAITranscriptionProvider(BaseTranscriptionProvider):
    """Uses OpenAI's Whisper API (cheaper than running locally if you lack GPU)."""

    def __init__(self, api_key: str):
        self._api_key = api_key

    @property
    def provider_name(self) -> str:
        return "openai_whisper_api"

    def transcribe(self, audio_file_path: str, language: str = "es") -> TranscriptionResult:
        import openai

        client = openai.OpenAI(api_key=self._api_key)
        with open(audio_file_path, "rb") as audio_file:
            result = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language=language,
                response_format="verbose_json",
            )

        return TranscriptionResult(
            text=result.text.strip(),
            language=language,
            confidence=0.9,
            duration_seconds=getattr(result, "duration", 0.0),
        )


class OpenAIFeedbackProvider(BaseFeedbackProvider):
    """Uses GPT to generate pedagogical feedback."""

    def __init__(self, api_key: str):
        self._api_key = api_key
        self._fallback = NLPFeedbackProvider()

    @property
    def provider_name(self) -> str:
        return "openai_gpt"

    def generate_feedback(self, expected_text: str, evaluation: EvaluationResult) -> FeedbackResult:
        try:
            return self._call_gpt(expected_text, evaluation)
        except Exception as e:
            logger.warning("OpenAI API failed (%s), falling back to NLP.", str(e))
            return self._fallback.generate_feedback(expected_text, evaluation)

    def _call_gpt(self, expected_text: str, evaluation: EvaluationResult) -> FeedbackResult:
        import json
        import re

        import openai

        client = openai.OpenAI(api_key=self._api_key)
        prompt = f"""Eres un profesor de lectura para niños de primer grado.
Texto esperado: "{expected_text}"
Precisión: {evaluation.accuracy:.1f}%
Palabras faltantes: {", ".join(evaluation.missing_words[:5]) or "ninguna"}

Responde SOLO con JSON: {{"overall_comment": "...", "suggestions": ["...", "...", "..."]}}"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.7,
        )

        raw = response.choices[0].message.content
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if match:
            data = json.loads(match.group())
            return FeedbackResult(
                overall_comment=data.get("overall_comment", ""),
                suggestions=data.get("suggestions", []),
                word_analysis=evaluation.word_analysis,
                correct_words=evaluation.correct_words,
                incorrect_words=evaluation.incorrect_words,
                missing_words=evaluation.missing_words,
            )
        return self._fallback.generate_feedback(expected_text, evaluation)
