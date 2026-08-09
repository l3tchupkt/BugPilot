from __future__ import annotations

import dataclasses
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True, slots=True, kw_only=True)
class Persona:
    """A virtual security research persona configuration."""

    id: str
    """Unique identifier for the persona (e.g. 'pentester')."""

    name: str
    """Display name for the persona."""

    description: str
    """Short description of the persona's role and capabilities."""

    system_prompt: str
    """The persona's core identity, workflow, and instructions."""

    capabilities: tuple[str, ...] = ()
    """List of abstract capabilities (e.g. 'recon', 'source-audit')."""

    tools: tuple[str, ...] = ()
    """List of allowed tool names."""

    allowed_subagents: tuple[str, ...] = ()
    """List of persona IDs this persona is allowed to spawn."""

    default_model: str | None = None
    """Optional default model alias to use for this persona."""

    temperature: float | None = None
    """Optional temperature override for this persona."""

    def extend(
        self,
        *,
        id: str | None = None,
        name: str | None = None,
        description: str | None = None,
        system_prompt: str | None = None,
        capabilities: tuple[str, ...] | None = None,
        tools: tuple[str, ...] | None = None,
        allowed_subagents: tuple[str, ...] | None = None,
        default_model: str | None = None,
        temperature: float | None = None,
    ) -> Persona:
        """Create a new persona extending this one with modified fields."""
        return dataclasses.replace(
            self,
            id=id if id is not None else self.id,
            name=name if name is not None else self.name,
            description=description if description is not None else self.description,
            system_prompt=system_prompt if system_prompt is not None else self.system_prompt,
            capabilities=capabilities if capabilities is not None else self.capabilities,
            tools=tools if tools is not None else self.tools,
            allowed_subagents=allowed_subagents if allowed_subagents is not None else self.allowed_subagents,
            default_model=default_model if default_model is not None else self.default_model,
            temperature=temperature if temperature is not None else self.temperature,
        )
