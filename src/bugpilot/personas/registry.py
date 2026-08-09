from __future__ import annotations

from bugpilot.personas.base import Persona


class PersonaRegistry:
    """Registry for discovering and loading personas."""

    _personas: dict[str, Persona] = {}

    @classmethod
    def register(cls, persona: Persona) -> None:
        """Register a new persona."""
        cls._personas[persona.id] = persona

    @classmethod
    def get(cls, id: str) -> Persona:
        """Get a persona by ID."""
        if id not in cls._personas:
            raise KeyError(f"Persona '{id}' not found in registry.")
        return cls._personas[id]

    @classmethod
    def list_all(cls) -> list[Persona]:
        """List all registered personas."""
        return list(cls._personas.values())

    @classmethod
    def load_builtins(cls) -> None:
        """Load built-in personas. Safe to call multiple times."""
        # Avoid circular imports by importing inside
        from bugpilot.personas.pentester import PENTESTER
        from bugpilot.personas.reporter import REPORTER
        from bugpilot.personas.researcher import RESEARCHER
        from bugpilot.personas.security_analyst import SECURITY_ANALYST
        from bugpilot.personas.triager import TRIAGER

        cls.register(PENTESTER)
        cls.register(SECURITY_ANALYST)
        cls.register(RESEARCHER)
        cls.register(TRIAGER)
        cls.register(REPORTER)
