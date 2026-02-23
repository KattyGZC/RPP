"""
EvaluationService — orchestrates the full reading evaluation pipeline:
1. Transcription (audio → text) via the configured provider
2. Text comparison (expected vs transcribed) using NLP
3. Feedback generation via the configured provider
4. Returns a complete EvaluationResult ready to be saved
"""
import logging
import os
import re
import tempfile
from dataclasses import asdict
from typing import Optional

from rapidfuzz import fuzz

from .factory import AIProviderFactory
from .providers.base import EvaluationResult, FeedbackResult, WordAnalysis

logger = logging.getLogger(__name__)

CORRECT_THRESHOLD = 0.85
PARTIAL_THRESHOLD = 0.60


class TextEvaluationService:
    """
    Pure NLP service: compares expected text against transcribed text.
    No AI API calls — fully deterministic and testable.
    """

    def normalize(self, text: str) -> str:
        text = text.lower()
        text = re.sub(r"[^\w\s]", "", text)
        return re.sub(r"\s+", " ", text).strip()

    def evaluate(self, expected_text: str, transcribed_text: str, max_score: float = 100.0) -> EvaluationResult:
        expected_words = self.normalize(expected_text).split()
        transcribed_words = self.normalize(transcribed_text).split()

        if not expected_words:
            return EvaluationResult(score=0.0, accuracy=0.0, transcription=transcribed_text)

        word_analysis: list[WordAnalysis] = []
        correct_words: list[str] = []
        incorrect_words: list[dict] = []
        missing_words: list[str] = []

        matched_transcribed = set()

        for expected_word in expected_words:
            best_similarity = 0.0
            best_match_idx = -1

            for idx, t_word in enumerate(transcribed_words):
                if idx in matched_transcribed:
                    continue
                similarity = fuzz.ratio(expected_word, t_word) / 100.0
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_match_idx = idx

            analysis = WordAnalysis(
                expected=expected_word,
                transcribed=transcribed_words[best_match_idx] if best_match_idx >= 0 else "",
                is_correct=best_similarity >= CORRECT_THRESHOLD,
                similarity=round(best_similarity, 3),
            )
            word_analysis.append(analysis)

            if best_similarity >= CORRECT_THRESHOLD:
                correct_words.append(expected_word)
                if best_match_idx >= 0:
                    matched_transcribed.add(best_match_idx)
            elif best_similarity >= PARTIAL_THRESHOLD:
                incorrect_words.append({
                    "expected": expected_word,
                    "got": transcribed_words[best_match_idx] if best_match_idx >= 0 else "",
                    "similarity": round(best_similarity, 3),
                })
                if best_match_idx >= 0:
                    matched_transcribed.add(best_match_idx)
            else:
                missing_words.append(expected_word)

        extra_words = [
            transcribed_words[i] for i in range(len(transcribed_words))
            if i not in matched_transcribed
        ]

        total = len(expected_words)
        # Partial credit: incorrect words get 50% of their similarity score
        partial_credit = sum(w["similarity"] * 0.5 for w in incorrect_words)
        effective_correct = len(correct_words) + partial_credit
        score = round((effective_correct / total) * max_score, 2)
        accuracy = round((len(correct_words) / total) * 100, 2)

        return EvaluationResult(
            score=score,
            accuracy=accuracy,
            transcription=transcribed_text,
            word_analysis=word_analysis,
            correct_words=correct_words,
            incorrect_words=incorrect_words,
            missing_words=missing_words,
            extra_words=extra_words,
        )


class EvaluationOrchestrator:
    """
    High-level service that coordinates transcription + evaluation + feedback.
    This is the single entry point for the evaluation feature.
    """

    def __init__(self):
        self._text_evaluator = TextEvaluationService()

    def evaluate_reading(
        self,
        audio_file_path: str,
        expected_text: str,
        max_score: float = 100.0,
        language: str = "es",
    ) -> dict:
        """
        Full pipeline:
        1. Transcribe audio
        2. Compare transcription to expected text
        3. Generate feedback
        4. Return serializable dict
        """
        # Step 1 — Transcription
        transcription_provider = AIProviderFactory.get_transcription_provider()
        logger.info("Transcribing with provider: %s", transcription_provider.provider_name)
        transcription = transcription_provider.transcribe(audio_file_path, language=language)

        # Step 2 — Text evaluation
        evaluation = self._text_evaluator.evaluate(
            expected_text=expected_text,
            transcribed_text=transcription.text,
            max_score=max_score,
        )

        # Step 3 — Feedback generation
        feedback_provider = AIProviderFactory.get_feedback_provider()
        logger.info("Generating feedback with provider: %s", feedback_provider.provider_name)
        feedback = feedback_provider.generate_feedback(expected_text, evaluation)

        return {
            "score": evaluation.score,
            "accuracy": evaluation.accuracy,
            "transcription": evaluation.transcription,
            "confidence": transcription.confidence,
            "duration_seconds": transcription.duration_seconds,
            "feedback": {
                "overall_comment": feedback.overall_comment,
                "suggestions": feedback.suggestions,
                "correct_words": feedback.correct_words,
                "incorrect_words": feedback.incorrect_words,
                "missing_words": feedback.missing_words,
                "word_analysis": [
                    {"expected": wa.expected, "transcribed": wa.transcribed,
                     "is_correct": wa.is_correct, "similarity": wa.similarity}
                    for wa in feedback.word_analysis
                ],
            },
        }

    @staticmethod
    def save_audio_temporarily(audio_file) -> str:
        """Saves an uploaded file to a temp location and returns the path."""
        suffix = os.path.splitext(audio_file.name)[-1] or ".webm"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            for chunk in audio_file.chunks():
                tmp.write(chunk)
            return tmp.name
