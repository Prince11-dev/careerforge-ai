"""AI Provider factory and configuration."""
from app.core.config import settings
from app.ai.base import AIProvider
from app.ai.mock_provider import MockAIProvider

class AIProviderFactory:
    """Factory for creating AI provider instances."""

    @staticmethod
    def get_provider() -> AIProvider:
        if settings.mock_ai_mode or settings.ai_provider == "mock":
            return MockAIProvider()
        # Future: OpenAIProvider, AnthropicProvider, etc.
        return MockAIProvider()

ai_provider = AIProviderFactory.get_provider()
