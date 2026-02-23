"""
AI Provider Factory — Factory Pattern.

Creates the correct transcription and feedback provider instances
based on environment configuration. New providers only need to be
added here; no other files need to change.
"""
import logging

from django.conf import settings

from .providers.base import BaseFeedbackProvider, BaseTranscriptionProvider

logger = logging.getLogger(__name__)


class AIProviderFactory:
    """
    Resolves which AI provider to use based on the application settings.
    Provider instances are singletons (created once, reused across requests).
    """

    _transcription_instance: BaseTranscriptionProvider = None
    _feedback_instance: BaseFeedbackProvider = None

    @classmethod
    def get_transcription_provider(cls) -> BaseTranscriptionProvider:
        if cls._transcription_instance is None:
            cls._transcription_instance = cls._create_transcription_provider()
        return cls._transcription_instance

    @classmethod
    def get_feedback_provider(cls) -> BaseFeedbackProvider:
        if cls._feedback_instance is None:
            cls._feedback_instance = cls._create_feedback_provider()
        return cls._feedback_instance

    @classmethod
    def _create_transcription_provider(cls) -> BaseTranscriptionProvider:
        provider_name = getattr(settings, "AI_TRANSCRIPTION_PROVIDER", "whisper_local")

        if provider_name == "whisper_local":
            from .providers.whisper_provider import WhisperLocalProvider
            model_size = getattr(settings, "WHISPER_MODEL_SIZE", "small")
            logger.info("Using transcription provider: WhisperLocal (model=%s)", model_size)
            return WhisperLocalProvider(model_size=model_size)

        if provider_name == "openai":
            api_key = getattr(settings, "OPENAI_API_KEY", None)
            if not api_key:
                raise ValueError("OPENAI_API_KEY must be set when AI_TRANSCRIPTION_PROVIDER=openai")
            from .providers.openai_provider import OpenAITranscriptionProvider
            logger.info("Using transcription provider: OpenAI Whisper API")
            return OpenAITranscriptionProvider(api_key=api_key)

        raise ValueError(f"Unknown transcription provider: '{provider_name}'. "
                         f"Valid options: 'whisper_local', 'openai'")

    @classmethod
    def _create_feedback_provider(cls) -> BaseFeedbackProvider:
        provider_name = getattr(settings, "AI_FEEDBACK_PROVIDER", "nlp_local")

        if provider_name == "nlp_local":
            from .providers.nlp_provider import NLPFeedbackProvider
            logger.info("Using feedback provider: NLP (local)")
            return NLPFeedbackProvider()

        if provider_name == "claude":
            api_key = getattr(settings, "ANTHROPIC_API_KEY", None)
            if not api_key:
                raise ValueError("ANTHROPIC_API_KEY must be set when AI_FEEDBACK_PROVIDER=claude")
            from .providers.claude_provider import ClaudeFeedbackProvider
            logger.info("Using feedback provider: Claude API")
            return ClaudeFeedbackProvider(api_key=api_key)

        if provider_name == "openai":
            api_key = getattr(settings, "OPENAI_API_KEY", None)
            if not api_key:
                raise ValueError("OPENAI_API_KEY must be set when AI_FEEDBACK_PROVIDER=openai")
            from .providers.openai_provider import OpenAIFeedbackProvider
            logger.info("Using feedback provider: OpenAI GPT")
            return OpenAIFeedbackProvider(api_key=api_key)

        raise ValueError(f"Unknown feedback provider: '{provider_name}'. "
                         f"Valid options: 'nlp_local', 'claude', 'openai'")
