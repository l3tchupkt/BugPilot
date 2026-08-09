from collections.abc import AsyncIterator
from typing import Any

from kosong.chat_provider import ChatProvider
from kosong.message import Message, TextPart, ThinkPart, ToolCall, ToolCallPart
from kosong.tooling import Tool

from bugpilot.providers.base import LLMProvider, LLMResponse, ResponseChunk, Usage


class KosongAdapter(LLMProvider):
    """Adapts a Kosong ChatProvider to the BugPilot LLMProvider interface."""

    def __init__(
        self,
        chat_provider: ChatProvider,
        supports_tools: bool = True,
        supports_reasoning: bool = False,
    ):
        self._chat_provider = chat_provider
        self._supports_tools = supports_tools
        self._supports_reasoning = supports_reasoning

    async def generate(
        self, messages: list[Message], tools: list[Tool] | None = None, **kwargs: Any
    ) -> LLMResponse:
        # We simulate generate by consuming the stream
        stream = await self.stream(messages, tools, **kwargs)

        content = ""
        reasoning_content = ""
        tool_calls: list[ToolCall] = []
        usage: Usage | None = None

        async for chunk in stream:
            content += chunk.text_delta
            reasoning_content += chunk.reasoning_delta
            if chunk.usage:
                usage = chunk.usage
            if chunk.tool_call:
                tool_calls.append(chunk.tool_call)

        return LLMResponse(
            content=content,
            tool_calls=tool_calls,
            finish_reason="stop",  # Simplified for now
            usage=usage,
            model=self._chat_provider.model_name,
            reasoning_content=reasoning_content if reasoning_content else None,
        )

    async def stream(
        self, messages: list[Message], tools: list[Tool] | None = None, **kwargs: Any
    ) -> AsyncIterator[ResponseChunk]:
        tools = tools or []

        # Optionally handle generation kwargs inside the adapter or pass to chat_provider
        # Some Kosong providers support `with_generation_kwargs`
        provider = self._chat_provider
        if hasattr(provider, "with_generation_kwargs") and kwargs:
            provider = provider.with_generation_kwargs(**kwargs)  # type: ignore

        kosong_stream = await provider.generate(
            system_prompt="",  # In Kosong, system prompt is often passed separately, but BugPilot Agent loop already includes it as `user`/`system` roles in `messages`. Wait, I need to check how BugPilot Agent loop passes system prompt.
            tools=tools,
            history=messages,
        )

        async for part in kosong_stream:
            chunk = ResponseChunk(id=kosong_stream.id)
            if isinstance(part, TextPart):
                chunk.text_delta = part.text
            elif isinstance(part, ThinkPart):
                chunk.reasoning_delta = part.think
            elif isinstance(part, ToolCall):
                chunk.tool_call = part
            elif isinstance(part, ToolCallPart):
                chunk.tool_call_delta = part.arguments_part

            if kosong_stream.usage:
                chunk.usage = Usage(
                    input_tokens=kosong_stream.usage.input,
                    output_tokens=kosong_stream.usage.output,
                )
            yield chunk

    def supports_tools(self) -> bool:
        return self._supports_tools

    def supports_reasoning(self) -> bool:
        return self._supports_reasoning
