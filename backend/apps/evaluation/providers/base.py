"""
Abstract base classes for AI providers — Strategy Pattern.

Adding a new provider means implementing these interfaces and registering
the provider in the factory. No other code needs to change.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List


@dataclass
class TranscriptionResult:
    """Output of any transcription provider."""
    text: str
    language: str
    confidence: float
    duration_seconds: float


@dataclass
class WordAnalysis:
    """Per-word evaluation result."""
    expected: str
    transcribed: str
    is_correct: bool
    similarity: float


@dataclass
class EvaluationResult:
    """
    Complete result of evaluating one reading attempt.
    Produced by TextEvaluationService and consumed by feedback providers.
    """
    score: float
    accuracy: float
    transcription: str
    word_analysis: List[WordAnalysis] = field(default_factory=list)
    correct_words: List[str] = field(default_factory=list)
    incorrect_words: List[dict] = field(default_factory=list)
    missing_words: List[str] = field(default_factory=list)
    extra_words: List[str] = field(default_factory=list)


@dataclass
class FeedbackResult:
    """
    Structured pedagogical feedback.
    Produced by any feedback provider.
    """
    overall_comment: str
    suggestions: List[str] = field(default_factory=list)
    word_analysis: List[WordAnalysis] = field(default_factory=list)
    correct_words: List[str] = field(default_factory=list)
    incorrect_words: List[dict] = field(default_factory=list)
    missing_words: List[str] = field(default_factory=list)


class BaseTranscriptionProvider(ABC):
    """
    Strategy interface for transcription.
    Implementations: WhisperLocalProvider, OpenAITranscriptionProvider.
    """

    @abstractmethod
    def transcribe(self, audio_file_path: str, language: str = "es") -> TranscriptionResult:
        """Transcribes audio file to text."""
        ...

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Human-readable provider name for logging."""
        ...


class BaseFeedbackProvider(ABC):
    """
    Strategy interface for feedback generation.
    Implementations: NLPFeedbackProvider, ClaudeFeedbackProvider, OpenAIFeedbackProvider.
    """

    @abstractmethod
    def generate_feedback(
        self,
        expected_text: str,
        evaluation: "EvaluationResult",
    ) -> FeedbackResult:
        """Generates pedagogical feedback from an evaluation result."""
        ...

    @property
    @abstractmethod
    def provider_name(self) -> str:
        ...
