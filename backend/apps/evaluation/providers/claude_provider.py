"""
Anthropic Claude feedback provider.
Activated when ANTHROPIC_API_KEY is set and AI_FEEDBACK_PROVIDER=claude.
Provides rich, pedagogical feedback powered by Claude.
"""
import logging

from .base import BaseFeedbackProvider, EvaluationResult, FeedbackResult
from .nlp_provider import NLPFeedbackProvider

logger = logging.getLogger(__name__)


class ClaudeFeedbackProvider(BaseFeedbackProvider):
    """
    Uses the Anthropic Claude API to generate rich, pedagogical feedback.
    Falls back to NLPFeedbackProvider if the API call fails.
    """

    def __init__(self, api_key: str):
        self._api_key = api_key
        self._fallback = NLPFeedbackProvider()

    @property
    def provider_name(self) -> str:
        return "claude"

    def generate_feedback(self, expected_text: str, evaluation: EvaluationResult) -> FeedbackResult:
        try:
            return self._call_claude(expected_text, evaluation)
        except Exception as e:
            logger.warning("Claude API failed (%s), falling back to NLP provider.", str(e))
            return self._fallback.generate_feedback(expected_text, evaluation)

    def _call_claude(self, expected_text: str, evaluation: EvaluationResult) -> FeedbackResult:
        import anthropic

        prompt = self._build_prompt(expected_text, evaluation)
        client = anthropic.Anthropic(api_key=self._api_key)

        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=512,
            messages=[{"role": "user", "content": prompt}],
        )

        raw_feedback = message.content[0].text
        return self._parse_claude_response(raw_feedback, evaluation)

    def _build_prompt(self, expected_text: str, evaluation: EvaluationResult) -> str:
        missing = ", ".join(evaluation.missing_words[:5]) if evaluation.missing_words else "ninguna"
        incorrect = (
            ", ".join(f'{w["expected"]}→{w.get("got", "?")}' for w in evaluation.incorrect_words[:5])
            if evaluation.incorrect_words else "ninguna"
        )
        return f"""Eres un profesor de lectura para niños de primer grado.
Un estudiante acaba de leer el siguiente texto en voz alta:

TEXTO ESPERADO: "{expected_text}"
TEXTO TRANSCRITO: "{evaluation.transcription}"

RESULTADOS:
- Precisión: {evaluation.accuracy:.1f}%
- Palabras faltantes o no pronunciadas: {missing}
- Palabras pronunciadas incorrectamente: {incorrect}

Por favor da retroalimentación pedagógica breve y alentadora en español.
Responde SOLO con este formato JSON:
{{
  "overall_comment": "comentario motivador en 1-2 oraciones",
  "suggestions": ["sugerencia 1", "sugerencia 2", "sugerencia 3"]
}}"""

    def _parse_claude_response(self, raw: str, evaluation: EvaluationResult) -> FeedbackResult:
        import json
        import re

        try:
            json_match = re.search(r'\{.*\}', raw, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                return FeedbackResult(
                    overall_comment=data.get("overall_comment", ""),
                    suggestions=data.get("suggestions", []),
                    word_analysis=evaluation.word_analysis,
                    correct_words=evaluation.correct_words,
                    incorrect_words=evaluation.incorrect_words,
                    missing_words=evaluation.missing_words,
                )
        except (json.JSONDecodeError, AttributeError):
            pass

        return self._fallback.generate_feedback("", evaluation)
