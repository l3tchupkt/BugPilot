"""Tests for AskUserQuestion description stability under plan mode."""

from __future__ import annotations

from pathlib import Path

from bugpilot.soul.agent import Agent
from bugpilot.soul.agent_loop import AgentLoop, Runtime
from bugpilot.soul.context import Context
from bugpilot.soul.toolset import Toolset
from bugpilot.tools.ask_user import _BASE_DESCRIPTION, AskUserQuestion


class TestAskUserDescriptionStability:
    def test_description_stays_static_when_soul_toggles_plan_mode(
        self, runtime: Runtime, tmp_path: Path
    ) -> None:
        """Agent plan mode toggles must not alter AskUserQuestion's description."""
        toolset = Toolset()
        tool = AskUserQuestion()
        toolset.add(tool)

        agent = Agent(
            name="Test Agent",
            system_prompt="Test system prompt.",
            toolset=toolset,
            runtime=runtime,
        )
        soul = AgentLoop(agent, context=Context(file_backend=tmp_path / "history.jsonl"))

        before = tool.base.description
        soul._set_plan_mode(True, source="tool")
        during = tool.base.description
        soul._set_plan_mode(False, source="tool")
        after = tool.base.description

        assert before == _BASE_DESCRIPTION
        assert during == _BASE_DESCRIPTION
        assert after == _BASE_DESCRIPTION
