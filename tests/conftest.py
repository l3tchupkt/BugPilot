"""Test configuration and fixtures."""

from __future__ import annotations

import os
import platform
import tempfile
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

import pytest
from kaos import get_current_kaos, reset_current_kaos, set_current_kaos
from kaos.local import LocalKaos
from kaos.path import KaosPath
from kosong.chat_provider.mock import MockChatProvider

from bugpilot.background import BackgroundTaskManager
from bugpilot.config import Config, get_default_config
from bugpilot.llm import ALL_MODEL_CAPABILITIES, LLM
from bugpilot.metadata import WorkDirMeta
from bugpilot.notifications import NotificationManager
from bugpilot.session import Session
from bugpilot.session_state import SessionState
from bugpilot.soul.agent import BuiltinSystemPromptArgs, LaborMarket, Runtime
from bugpilot.soul.approval import Approval
from bugpilot.soul.denwarenji import DenwaRenji
from bugpilot.soul.toolset import Toolset
from bugpilot.subagents import AgentTypeDefinition, ToolPolicy
from bugpilot.tools.agent import Agent as AgentTool
from bugpilot.tools.background import (
    TaskList,
    TaskOutput,
    TaskStop,
)
from bugpilot.tools.dmail import SendDMail
from bugpilot.tools.file.glob import Glob
from bugpilot.tools.file.grep_local import Grep
from bugpilot.tools.file.read import ReadFile
from bugpilot.tools.file.read_media import ReadMediaFile
from bugpilot.tools.file.replace import StrReplaceFile
from bugpilot.tools.file.write import WriteFile
from bugpilot.tools.shell import Shell
from bugpilot.tools.think import Think
from bugpilot.tools.todo import SetTodoList
from bugpilot.utils.environment import Environment
from bugpilot.wire.file import WireFile


@pytest.fixture
def config() -> Config:
    """Create a Config instance."""
    conf = get_default_config()
    return conf


@pytest.fixture
def llm() -> LLM:
    """Create a LLM instance."""
    return LLM(
        provider=MockChatProvider([]),
        max_context_size=100_000,
        capabilities=ALL_MODEL_CAPABILITIES,
    )


@pytest.fixture
def temp_work_dir() -> Generator[KaosPath]:
    """Create a temporary working directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        original_cwd = Path.cwd()
        p = Path(tmpdir).resolve()
        os.chdir(p)
        token = set_current_kaos(LocalKaos())
        try:
            yield KaosPath.unsafe_from_local_path(p)
        finally:
            reset_current_kaos(token)
            os.chdir(original_cwd)


@pytest.fixture
def temp_share_dir() -> Generator[Path]:
    """Create a temporary shared directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def builtin_args(temp_work_dir: KaosPath) -> BuiltinSystemPromptArgs:
    """Create builtin arguments with temporary work directory."""
    return BuiltinSystemPromptArgs(
        BUGPILOT_NOW="1970-01-01T00:00:00+00:00",
        BUGPILOT_WORK_DIR=temp_work_dir,
        BUGPILOT_WORK_DIR_LS="Test ls content",
        BUGPILOT_AGENTS_MD="Test agents content",
        BUGPILOT_SKILLS="No skills found.",
        BUGPILOT_ADDITIONAL_DIRS_INFO="",
        BUGPILOT_OS="macOS",
        BUGPILOT_SHELL="bash (`/bin/bash`)",
    )


@pytest.fixture
def denwa_renji() -> DenwaRenji:
    """Create a DenwaRenji instance."""
    return DenwaRenji()


@pytest.fixture
def session(temp_work_dir: KaosPath, temp_share_dir: Path) -> Session:
    """Create a Session instance."""
    return Session(
        id="test",
        work_dir=temp_work_dir,
        work_dir_meta=WorkDirMeta(path=str(temp_work_dir), kaos=get_current_kaos().name),
        context_file=temp_share_dir / "context.jsonl",
        wire_file=WireFile(path=temp_share_dir / "wire.jsonl"),
        state=SessionState(),
        title="Test Session",
        updated_at=0.0,
    )


@pytest.fixture
def approval() -> Approval:
    """Create a Approval instance."""
    return Approval(yolo=True)


@pytest.fixture
def labor_market() -> LaborMarket:
    """Create a LaborMarket instance."""
    return LaborMarket()


@pytest.fixture
def environment() -> Environment:
    """Create an Environment instance."""
    if platform.system() == "Windows":
        return Environment(
            os_kind="Windows",
            os_arch="x86_64",
            os_version="1.0",
            shell_name="bash",
            shell_path=KaosPath(r"C:\Program Files\Git\bin\bash.exe"),
        )
    else:
        return Environment(
            os_kind="Unix",
            os_arch="aarch64",
            os_version="1.0",
            shell_name="bash",
            shell_path=KaosPath("/bin/bash"),
        )


@pytest.fixture
def runtime(
    config: Config,
    llm: LLM,
    builtin_args: BuiltinSystemPromptArgs,
    denwa_renji: DenwaRenji,
    session: Session,
    approval: Approval,
    labor_market: LaborMarket,
    environment: Environment,
) -> Runtime:
    """Create a Runtime instance."""
    notifications = NotificationManager(
        session.context_file.parent / "notifications", config.notifications
    )
    rt = Runtime(
        config=config,
        llm=llm,
        builtin_args=builtin_args,
        denwa_renji=denwa_renji,
        session=session,
        approval=approval,
        labor_market=labor_market,
        environment=environment,
        notifications=notifications,
        background_tasks=BackgroundTaskManager(
            session,
            config.background,
            notifications=notifications,
        ),
        skills={},
        #         oauth=OAuthManager(config),
        additional_dirs=[],
        skills_dirs=[],
        role="root",
    )
    rt.labor_market.add_builtin_type(
        AgentTypeDefinition(
            name="mocker",
            description="The mock agent for testing purposes.",
            agent_file=Path("/tmp/mocker-agent.yaml"),
            tool_policy=ToolPolicy(mode="inherit"),
        )
    )
    return rt


@pytest.fixture
def toolset() -> Toolset:
    return Toolset()


@contextmanager
def tool_call_context(tool_name: str) -> Generator[None]:
    """Create a tool call context."""
    from bugpilot.soul.toolset import current_tool_call
    from bugpilot.wire.types import ToolCall

    token = current_tool_call.set(
        ToolCall(id="test", function=ToolCall.FunctionBody(name=tool_name, arguments=None))
    )
    try:
        yield
    finally:
        current_tool_call.reset(token)


@pytest.fixture
def agent_tool(runtime: Runtime) -> AgentTool:
    """Create an Agent tool instance."""
    return AgentTool(runtime)


@pytest.fixture
def send_dmail_tool(denwa_renji: DenwaRenji) -> SendDMail:
    """Create a SendDMail tool instance."""
    return SendDMail(denwa_renji)


@pytest.fixture
def think_tool() -> Think:
    """Create a Think tool instance."""
    return Think()


@pytest.fixture
def set_todo_list_tool(runtime: Runtime) -> SetTodoList:
    """Create a SetTodoList tool instance."""
    return SetTodoList(runtime)


@pytest.fixture
def shell_tool(approval: Approval, environment: Environment, runtime: Runtime) -> Generator[Shell]:
    """Create a Shell tool instance."""
    with tool_call_context("Shell"):
        yield Shell(approval, environment, runtime)


@pytest.fixture
def task_list_tool(runtime: Runtime) -> Generator[TaskList]:
    with tool_call_context("TaskList"):
        yield TaskList(runtime)


@pytest.fixture
def task_output_tool(runtime: Runtime) -> TaskOutput:
    with tool_call_context("TaskOutput"):
        return TaskOutput(runtime)


@pytest.fixture
def task_stop_tool(runtime: Runtime, approval: Approval) -> Generator[TaskStop]:
    with tool_call_context("TaskStop"):
        yield TaskStop(runtime, approval)


@pytest.fixture
def read_file_tool(runtime: Runtime) -> ReadFile:
    """Create a ReadFile tool instance."""
    return ReadFile(runtime)


@pytest.fixture
def read_media_file_tool(runtime: Runtime) -> ReadMediaFile:
    """Create a ReadMediaFile tool instance."""
    return ReadMediaFile(runtime)


@pytest.fixture
def glob_tool(runtime: Runtime) -> Glob:
    """Create a Glob tool instance."""
    return Glob(runtime)


@pytest.fixture
def grep_tool() -> Grep:
    """Create a Grep tool instance."""
    return Grep()


@pytest.fixture
def write_file_tool(runtime: Runtime, approval: Approval) -> Generator[WriteFile]:
    """Create a WriteFile tool instance."""
    with tool_call_context("WriteFile"):
        yield WriteFile(runtime, approval)


@pytest.fixture
def str_replace_file_tool(runtime: Runtime, approval: Approval) -> Generator[StrReplaceFile]:
    """Create a StrReplaceFile tool instance."""
    with tool_call_context("StrReplaceFile"):
        yield StrReplaceFile(runtime, approval)


# misc fixtures


@pytest.fixture
def outside_file() -> Generator[Path]:
    """Return a path to a file outside the working directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir) / "outside_file.txt"
