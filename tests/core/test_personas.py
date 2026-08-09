import pytest

from bugpilot.personas.base import Persona
from bugpilot.personas.registry import PersonaRegistry
from bugpilot.agentspec import ResolvedAgentSpec


def test_persona_creation_and_extension():
    p1 = Persona(
        id="base-p",
        name="Base Persona",
        description="A test base persona",
        system_prompt="You are a base persona.",
        capabilities=("test",),
    )
    
    assert p1.name == "Base Persona"
    
    p2 = p1.extend(id="extended-p", name="Extended")
    assert p2.id == "extended-p"
    assert p2.name == "Extended"
    assert p2.capabilities == ("test",)


def test_persona_registry():
    PersonaRegistry.load_builtins()
    
    # Check that builtins are loaded
    pentester = PersonaRegistry.get("pentester")
    assert pentester.name == "Pentester"
    
    # Check listing
    all_p = PersonaRegistry.list_all()
    assert len(all_p) >= 5
    
    # Missing persona
    with pytest.raises(KeyError):
        PersonaRegistry.get("missing-persona-12345")


def test_persona_to_agent_spec():
    p = Persona(
        id="test-spec",
        name="Spec Test",
        description="Desc",
        system_prompt="System Prompt",
        capabilities=("a",),
        tools=("Shell",),
        allowed_subagents=("sub-a",),
        default_model="gpt-4o",
    )
    
    spec = ResolvedAgentSpec.from_persona(p)
    assert spec.name == "Spec Test"
    assert spec.system_prompt == "System Prompt"
    assert "Shell" in spec.tools
    assert "sub-a" in spec.subagents
    assert spec.model == "gpt-4o"
