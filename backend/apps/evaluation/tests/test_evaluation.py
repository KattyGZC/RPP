from django.test import TestCase

from apps.evaluation.providers.nlp_provider import NLPFeedbackProvider
from apps.evaluation.providers.base import EvaluationResult, WordAnalysis
from apps.evaluation.services import TextEvaluationService


class TextEvaluationServiceTests(TestCase):
    def setUp(self):
        self.service = TextEvaluationService()

    def test_perfect_match(self):
        result = self.service.evaluate("el gato es bonito", "el gato es bonito", max_score=100.0)
        self.assertEqual(result.accuracy, 100.0)
        self.assertGreaterEqual(result.score, 95.0)
        self.assertEqual(result.missing_words, [])

    def test_partial_match(self):
        result = self.service.evaluate(
            "el sol sale por el oriente",
            "el sol sale por",
            max_score=100.0,
        )
        self.assertLess(result.accuracy, 100.0)
        self.assertGreater(len(result.missing_words), 0)

    def test_empty_transcription(self):
        result = self.service.evaluate("el gato es bonito", "", max_score=100.0)
        self.assertEqual(result.score, 0.0)
        self.assertEqual(result.accuracy, 0.0)

    def test_normalize_removes_punctuation(self):
        normalized = self.service.normalize("¡Hola, mundo!")
        self.assertEqual(normalized, "hola mundo")

    def test_fuzzy_matching_typo(self):
        # "gato" vs "gatto" — should still count as close enough
        result = self.service.evaluate("el gato", "el gatto", max_score=100.0)
        self.assertGreater(result.accuracy, 50.0)

    def test_word_analysis_length_matches_expected(self):
        expected = "el perro corre rapido"
        result = self.service.evaluate(expected, "el perro corre lento", max_score=100.0)
        self.assertEqual(len(result.word_analysis), len(expected.split()))


class NLPFeedbackProviderTests(TestCase):
    def setUp(self):
        self.provider = NLPFeedbackProvider()

    def _make_evaluation(self, accuracy: float) -> EvaluationResult:
        return EvaluationResult(
            score=accuracy,
            accuracy=accuracy,
            transcription="test",
        )

    def test_excellent_comment_for_high_accuracy(self):
        feedback = self.provider.generate_feedback("test", self._make_evaluation(95.0))
        self.assertIn("Excelente", feedback.overall_comment)

    def test_encouraging_comment_for_low_accuracy(self):
        feedback = self.provider.generate_feedback("test", self._make_evaluation(20.0))
        self.assertTrue(len(feedback.overall_comment) > 0)

    def test_suggestions_always_provided(self):
        feedback = self.provider.generate_feedback("test", self._make_evaluation(50.0))
        self.assertIsInstance(feedback.suggestions, list)
        self.assertGreater(len(feedback.suggestions), 0)
