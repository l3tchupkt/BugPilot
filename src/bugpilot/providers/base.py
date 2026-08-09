import abc
from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import Any

from kosong.message import Message, ToolCall
from kosong.tooling import Tool

@dataclass
class Usage:
    input_tokens: int
    output_tokens: int

@dataclass
class LLMResponse:
    content: str
    tool_calls: list[ToolCall]
    finish_reason: str | None
    usage: Usage | None
    model: str
    reasoning_content: str | None = None

@dataclass
class ResponseChunk:
    id: str | None = None
    text_delta: str = ""
    reasoning_delta: str = ""
    tool_call: ToolCall | None = None
    tool_call_delta: str | None = None
    usage: Usage | None = None

class LLMProvider(abc.ABC):
    """Abstract base class for all BugPilot LLM providers."""
    
    @abc.abstractmethod
    async def generate(
        self, 
        messages: list[Message], 
        tools: list[Tool] | None = None, 
        **kwargs: Any
    ) -> LLMResponse:
        """Generate a complete response from the LLM."""
        ...

    @abc.abstractmethod
    async def stream(
        self, 
        messages: list[Message], 
        tools: list[Tool] | None = None, 
        **kwargs: Any
    ) -> AsyncIterator[ResponseChunk]:
        """Stream a response from the LLM."""
        ...
        
    @abc.abstractmethod
    def supports_tools(self) -> bool:
        """Returns True if the provider supports tool usage."""
        ...

    @abc.abstractmethod
    def supports_reasoning(self) -> bool:
        """Returns True if the provider supports specialized reasoning."""
        ...
