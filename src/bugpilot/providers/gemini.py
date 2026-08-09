from typing import Any

from kosong.contrib.chat_provider.google_genai import GoogleGenAI
from bugpilot.providers.kosong_adapter import KosongAdapter

class GeminiProvider(KosongAdapter):
    """Gemini provider adapter."""
    
    def __init__(self, model: str, api_key: str | None, base_url: str | None, default_headers: dict[str, str] | None = None, **kwargs: Any):
        chat_provider = GoogleGenAI(
            model=model,
            api_key=api_key,
            base_url=base_url,
            default_headers=default_headers,
            **kwargs
        )
        super().__init__(chat_provider, supports_tools=True, supports_reasoning=False)
