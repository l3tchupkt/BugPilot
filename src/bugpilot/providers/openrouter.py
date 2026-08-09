from typing import Any

from bugpilot.providers.openai_compatible import OpenAICompatibleProvider


class OpenRouterProvider(OpenAICompatibleProvider):
    """OpenRouter provider adapter extending OpenAICompatibleProvider."""

    def __init__(
        self,
        model: str,
        api_key: str | None,
        base_url: str | None,
        default_headers: dict[str, str] | None = None,
        **kwargs: Any,
    ):
        # Inject OpenRouter default base URL if not provided
        if not base_url:
            base_url = "https://openrouter.ai/api/v1"

        super().__init__(
            model=model,
            api_key=api_key,
            base_url=base_url,
            default_headers=default_headers,
            **kwargs,
        )
