"""
NLP-based feedback provider using spaCy and rapidfuzz.
Free, local, no API required. Provides detailed word-level feedback in Spanish.
"""
import logging
from typing import List

from rapidfuzz import fuzz

from .base import BaseFeedbackProvider, EvaluationResult, FeedbackResult, WordAnalysis

logger = logging.getLogger(__name__)

# Similarity threshold: words are "correct" if ≥ this score
CORRECT_THRESHOLD = 0.85
PARTIAL_THRESHOLD = 0.60


class NLPFeedbackProvider(BaseFeedbackProvider):
    """
    Generates structured feedback using fuzzy string matching.
    Provides word-level analysis without any external API.
    """

    @property
    def provider_name(self) -> str:
        return "nlp_local"

    def generate_feedback(self, expected_text: str, evaluation: EvaluationResult) -> FeedbackResult:
        overall_comment = self._build_overall_comment(evaluation.accuracy)
        suggestions = self._build_suggestions(evaluation)

        return FeedbackResult(
            overall_comment=overall_comment,
            suggestions=suggestions,
            word_analysis=evaluation.word_analysis,
            correct_words=evaluation.correct_words,
            incorrect_words=evaluation.incorrect_words,
            missing_words=evaluation.missing_words,
        )

    def _build_overall_comment(self, accuracy: float) -> str:
        if accuracy >= 90:
            return "¡Excelente lectura! Tu pronunciación es muy precisa."
        if accuracy >= 75:
            return "¡Muy bien! Tienes una buena lectura, sigue practicando."
        if accuracy >= 60:
            return "Buen intento. Con más práctica mejorarás bastante."
        if accuracy >= 40:
            return "Vas por buen camino. Intenta leer más despacio y con claridad."
        return "Sigue intentándolo. La práctica diaria te ayudará a mejorar."

    def _build_suggestions(self, evaluation: EvaluationResult) -> List[str]:
        suggestions = []

        if evaluation.missing_words:
            missing_sample = ", ".join(f'"{w}"' for w in evaluation.missing_words[:3])
            suggestions.append(f"Palabras que no se escucharon: {missing_sample}. Intenta pronunciarlas más claro.")

        difficult_words = [
            w for w in evaluation.incorrect_words
            if isinstance(w, dict) and w.get("similarity", 1.0) < 0.70
        ]
        if difficult_words:
            words_str = ", ".join(f'"{w["expected"]}"' for w in difficult_words[:3])
            suggestions.append(f"Practica estas palabras: {words_str}.")

        if evaluation.accuracy < 50:
            suggestions.append("Intenta leer el texto en voz alta varias veces antes de grabarte.")

        if not suggestions:
            suggestions.append("Continúa con el siguiente ejercicio para seguir mejorando.")

        return suggestions
