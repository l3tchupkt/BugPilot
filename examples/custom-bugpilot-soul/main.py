import asyncio
import os
from pathlib import Path
from typing import override

from bugpilot.auth.oauth import OAuthManager
from bugpilot.soul.bugpilotsoul import Agent
from kaos.path import KaosPath
from kosong.tooling import CallableTool2, ToolError, ToolOk, Toolset
from kosong.tooling.simple import SimpleToolset
from pydantic import BaseModel, Field, SecretStr

from bugpilot.config import LLMModel, LLMProvider, get_default_config
from bugpilot.llm import LLM, create_llm
from bugpilot.session import Session
from bugpilot.soul.agent import Agent, Runtime
from bugpilot.soul.context import Context
from bugpilot.ui.shell import Shell
from bugpilot.wire.types import ContentPart, ToolReturnValue


class HabugpilotSoul(Agent):
    @staticmethod
    async def create(
        llm: LLM | None,
        system_prompt: str,
        toolset: Toolset,
        session: Session | None = None,
        work_dir: Path | None = None,
    ) -> "HabugpilotSoul":
        config = get_default_config()
        kaos_work_dir = KaosPath.unsafe_from_local_path(work_dir) if work_dir else KaosPath.cwd()
        session = session or await Session.create(kaos_work_dir)
        runtime = await Runtime.create(
            config=config,
            oauth=OAuthManager(config),
            llm=llm,
            session=session,
            yolo=True,
        )
        agent = Agent(
            name="HabugpilotAgent",
            system_prompt=system_prompt,
            toolset=toolset,
            runtime=runtime,
        )
        context = Context(session.context_file)
        return HabugpilotSoul(agent, context=context)

    @property
    @override
    def name(self) -> str:
        return "Habugpilot"

    @override
    async def run(
        self,
        user_input: str | list[ContentPart],
        *,
        skip_user_prompt_hook: bool = False,
    ) -> None:
        if not self._context.history:
            await self._context.restore()
        await super().run(user_input, skip_user_prompt_hook=skip_user_prompt_hook)


class MyBashParams(BaseModel):
    command: str = Field(description="The bash command to execute.")


class MyBashTool(CallableTool2):
    name: str = "MyBashTool"
    description: str = "A tool to execute bash commands."
    params: type[MyBashParams] = MyBashParams

    async def __call__(self, params: MyBashParams) -> ToolReturnValue:
        import subprocess

        result = subprocess.run(params.command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            return ToolError(
                output=result.stdout,
                message=f"Command failed with error: {result.stderr}",
                brief="Bash command failed",
            )
        return ToolOk(output=result.stdout)


async def main():
    toolset = SimpleToolset()
    toolset += MyBashTool()

    soul = await HabugpilotSoul.create(
        llm=create_llm(
            LLMProvider(
                type="bugpilot",
                base_url=os.getenv("BUGPILOT_BASE_URL") or "https://api.bugpilot.ai/v1",
                api_key=SecretStr(os.getenv("BUGPILOT_API_KEY") or ""),
            ),
            LLMModel(
                provider="bugpilot",
                model="bugpilot-k2-turbo-preview",
                max_context_size=250_000,
            ),
        ),
        system_prompt="You are Habugpilot, an AI assistant that helps users with various tasks.",
        toolset=toolset,
    )
    ui = Shell(soul)
    await ui.run()


if __name__ == "__main__":
    asyncio.run(main())
