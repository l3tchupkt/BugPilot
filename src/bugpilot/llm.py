from __future__ import annotations

import json
import os
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Literal, cast, get_args

from kosong.message import (
    AudioURLPart,
    ImageURLPart,
    Message,
    TextPart,
    ThinkPart,
    VideoURLPart,
)
from kosong.tooling import Tool

if TYPE_CHECKING:
    from bugpilot.config import Config, LLMModel
    from bugpilot.config import LLMProvider as ConfigLLMProvider
    from bugpilot.providers.base import LLMProvider

type ProviderType = Literal[
    "openai",
    "anthropic",
    "gemini",
    "openai-compatible",
    "openrouter",
    "together-ai",
    "ollama",
]

type ModelCapability = Literal["image_in", "video_in", "thinking", "always_thinking"]
ALL_MODEL_CAPABILITIES: set[ModelCapability] = set(get_args(ModelCapability.__value__))
DEFAULT_UNKNOWN_CONTEXT_COMPLETION_TOKENS = 32_000
DEFAULT_COMPLETION_TOKEN_SAFETY_MARGIN = 1_024
MEDIA_TOKEN_ESTIMATE = 2_000


@dataclass(slots=True)
class LLM:
    provider: LLMProvider
    max_context_size: int
    capabilities: set[ModelCapability]
    model_config: LLMModel | None = None
    provider_config: ConfigLLMProvider | None = None


def compute_max_completion_tokens(
    *,
    max_context_size: int,
    input_tokens: int,
    response_budget: int | None,
    fallback_budget: int = DEFAULT_UNKNOWN_CONTEXT_COMPLETION_TOKENS,
) -> int:
    """Compute the BugPilot completion cap from the hard cap and remaining context."""
    if max_context_size <= 0:
        return max(1, response_budget if response_budget is not None else fallback_budget)

    input_tokens = max(0, input_tokens)
    remaining = max(1, max_context_size - input_tokens)
    requested = response_budget if response_budget is not None else max_context_size
    return max(1, min(requested, remaining))


def estimate_request_tokens(
    system_prompt: str,
    tools: Sequence[Tool],
    history: Sequence[Message],
) -> int:
    """Estimate all token-bearing parts of a chat request.

    The estimate is deliberately request-scoped: unlike ``Context.token_count_with_pending``,
    it includes the system prompt, tool schemas, message metadata, tool calls, and media. Exact
    tokenization is provider/model specific, so callers should still reserve a small safety
    margin when using the result to derive a hard completion limit.
    """
    return (
        _estimate_text_tokens(system_prompt)
        + sum(_estimate_tool_tokens(tool) for tool in tools)
        + sum(_estimate_message_tokens(message) for message in history)
    )


def estimate_message_tokens(messages: Sequence[Message]) -> int:
    """Estimate token-bearing content for messages added outside the main context."""
    return sum(_estimate_message_tokens(message) for message in messages)


def _estimate_text_tokens(text: str) -> int:
    ascii_count = sum(char.isascii() for char in text)
    non_ascii_count = len(text) - ascii_count
    return (ascii_count + 3) // 4 + non_ascii_count


def _estimate_tool_tokens(tool: Tool) -> int:
    return (
        _estimate_text_tokens(tool.name)
        + _estimate_text_tokens(tool.description)
        + _estimate_text_tokens(
            json.dumps(tool.parameters, ensure_ascii=False, separators=(",", ":"))
        )
    )


def _estimate_message_tokens(message: Message) -> int:
    total = _estimate_text_tokens(message.role)
    if message.name:
        total += _estimate_text_tokens(message.name)
    if message.tool_call_id:
        total += _estimate_text_tokens(message.tool_call_id)

    for part in message.content:
        if isinstance(part, TextPart):
            total += _estimate_text_tokens(part.text)
        elif isinstance(part, ThinkPart):
            total += _estimate_text_tokens(part.think)
        elif isinstance(part, (ImageURLPart, AudioURLPart, VideoURLPart)):
            total += MEDIA_TOKEN_ESTIMATE
        else:
            total += _estimate_text_tokens(part.model_dump_json(exclude_none=True))

    for tool_call in message.tool_calls or ():
        total += _estimate_text_tokens(tool_call.id)
        total += _estimate_text_tokens(tool_call.function.name)
        total += _estimate_text_tokens(tool_call.function.arguments or "")
        if tool_call.extras:
            total += _estimate_text_tokens(
                json.dumps(tool_call.extras, ensure_ascii=False, separators=(",", ":"))
            )
    return total


def model_display_name(model_name: str | None, model: LLMModel | None = None) -> str:
    if model is not None and model.display_name:
        return model.display_name
    if not model_name:
        return ""
    if model_name in ("bugpilot-for-coding", "bugpilot-code"):
        return "bugpilot-for-coding"
    return model_name


def augment_provider_with_env_vars(provider: ConfigLLMProvider, model: LLMModel) -> dict[str, str]:
    """Override provider/model settings from environment variables."""
    applied: dict[str, str] = {}
    return applied


def clone_llm_with_model_alias(
    llm: LLM | None,
    config: Config,
    model_alias: str | None,
    *,
    session_id: str,
) -> LLM | None:
    if model_alias is None:
        return llm
    if model_alias not in config.models:
        raise KeyError(f"Unknown model alias: {model_alias}")

    from bugpilot.providers.registry import ProviderRegistry

    provider = ProviderRegistry.create(config, model_alias, session_id=session_id)
    model = config.models[model_alias]

    return LLM(
        provider=provider,
        max_context_size=model.max_context_size,
        capabilities=derive_model_capabilities(model),
        model_config=model,
    )


def derive_model_capabilities(model: LLMModel) -> set[ModelCapability]:
    capabilities = set(model.capabilities or ())
    # Models with "thinking" in their name are always-thinking models
    if "thinking" in model.model.lower() or "reason" in model.model.lower():
        capabilities.update(("thinking", "always_thinking"))
    # These models support thinking but can be toggled on/off
    elif model.model in {"bugpilot-for-coding", "bugpilot-code"}:
        capabilities.update(("thinking", "image_in", "video_in"))
    return capabilities


def _load_scripted_echo_scripts() -> list[str]:
    script_path = os.getenv("BUGPILOT_SCRIPTED_ECHO_SCRIPTS")
    if not script_path:
        raise ValueError("BUGPILOT_SCRIPTED_ECHO_SCRIPTS is required for _scripted_echo.")
    path = Path(script_path).expanduser()
    if not path.exists():
        raise ValueError(f"Scripted echo file not found: {path}")
    text = path.read_text(encoding="utf-8")
    try:
        data: object = json.loads(text)
    except json.JSONDecodeError:
        scripts = [chunk.strip() for chunk in text.split("\n---\n") if chunk.strip()]
        if scripts:
            return scripts
        raise ValueError(
            "Scripted echo file must be a JSON array of strings or a text file "
            "split by '\\n---\\n'."
        ) from None
    if isinstance(data, list):
        data_list = cast(list[object], data)
        if all(isinstance(item, str) for item in data_list):
            return cast(list[str], data_list)
    raise ValueError("Scripted echo JSON must be an array of strings.")
