from bugpilot.config import Config
from bugpilot.providers.base import LLMProvider


class ProviderRegistry:
    """Registry for initializing LLM providers from configuration."""

    @classmethod
    def create(
        cls, config: Config, model_alias: str, *, session_id: str | None = None
    ) -> LLMProvider:
        """Create an LLMProvider instance based on the configuration."""
        # Support new `[provider]` structure
        if config.provider:
            model_name = config.provider.model
            provider_name = config.provider.name
        else:
            # Check configured models
            if model_alias in config.models:
                model_config = config.models[model_alias]
                model_name = model_config.model
                provider_name = model_config.provider
            else:
                # Dynamic fallback: parse `provider_name/model_name`
                if "/" in model_alias:
                    provider_name, model_name = model_alias.split("/", 1)
                else:
                    raise KeyError(f"Unknown model alias: {model_alias}")

        if provider_name not in config.providers:
            raise KeyError(f"Provider {provider_name} not found in configuration")

        provider_config = config.providers[provider_name]

        # Determine API key
        api_key = None
        if provider_config.api_key_env:
            import os

            api_key = os.getenv(provider_config.api_key_env)
        if not api_key and provider_config.api_key:
            api_key = provider_config.api_key.get_secret_value()

        provider_type = provider_config.type

        # Instantiate appropriate provider
        if provider_type == "openai":
            from bugpilot.providers.openai import OpenAIProvider

            return OpenAIProvider(
                model=model_name,
                api_key=api_key,
                base_url=provider_config.base_url,
                default_headers=provider_config.custom_headers,
            )

        elif provider_type == "anthropic":
            from bugpilot.providers.anthropic import AnthropicProvider

            return AnthropicProvider(
                model=model_name,
                api_key=api_key,
                base_url=provider_config.base_url,
                default_headers=provider_config.custom_headers,
            )

        elif provider_type == "gemini":
            from bugpilot.providers.gemini import GeminiProvider

            return GeminiProvider(
                model=model_name,
                api_key=api_key,
                base_url=provider_config.base_url,
                default_headers=provider_config.custom_headers,
            )

        elif provider_type == "openai-compatible" or provider_type == "openai_responses":
            from bugpilot.providers.openai_compatible import OpenAICompatibleProvider

            return OpenAICompatibleProvider(
                model=model_name,
                api_key=api_key,
                base_url=provider_config.base_url,
                default_headers=provider_config.custom_headers,
            )

        elif provider_type == "openrouter":
            from bugpilot.providers.openrouter import OpenRouterProvider

            return OpenRouterProvider(
                model=model_name,
                api_key=api_key,
                base_url=provider_config.base_url,
                default_headers=provider_config.custom_headers,
            )

        elif provider_type == "together-ai":
            from bugpilot.providers.together_ai import TogetherAIProvider

            return TogetherAIProvider(
                model=model_name,
                api_key=api_key,
                base_url=provider_config.base_url,
                default_headers=provider_config.custom_headers,
            )

        elif provider_type == "ollama":
            from bugpilot.providers.ollama import OllamaProvider

            return OllamaProvider(
                model=model_name,
                api_key=api_key,
                base_url=provider_config.base_url,
                default_headers=provider_config.custom_headers,
            )

        else:
            raise ValueError(f"Unsupported provider type: {provider_type}")
