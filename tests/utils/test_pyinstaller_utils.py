from __future__ import annotations

import platform
import sys
from pathlib import Path

from inline_snapshot import snapshot


def test_pyinstaller_datas():
    from bugpilot.utils.pyinstaller import datas

    project_root = Path(__file__).parent.parent.parent
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    site_packages = f".venv/lib/python{python_version}/site-packages"
    rg_binary = "rg.exe" if platform.system() == "Windows" else "rg"
    has_rg_binary = (project_root / "src/bugpilot/deps/bin" / rg_binary).exists()
    datas = [
        (
            Path(path)
            .relative_to(project_root)
            .as_posix()
            .replace(".venv/Lib/site-packages", site_packages),
            Path(dst).as_posix(),
        )
        for path, dst in datas
    ]

    datas = [(p, d) for p, d in datas if "web/static" not in d and "vis/static" not in d]

    expected_datas = [
        (
            f"{site_packages}/dateparser/data/dateparser_tz_cache.pkl",
            "dateparser/data",
        ),
        (
            f"{site_packages}/fastmcp/../fastmcp-3.2.4.dist-info/INSTALLER",
            "fastmcp/../fastmcp-3.2.4.dist-info",
        ),
        (
            f"{site_packages}/fastmcp/../fastmcp-3.2.4.dist-info/METADATA",
            "fastmcp/../fastmcp-3.2.4.dist-info",
        ),
        (
            f"{site_packages}/fastmcp/../fastmcp-3.2.4.dist-info/RECORD",
            "fastmcp/../fastmcp-3.2.4.dist-info",
        ),
        (
            f"{site_packages}/fastmcp/../fastmcp-3.2.4.dist-info/REQUESTED",
            "fastmcp/../fastmcp-3.2.4.dist-info",
        ),
        (
            f"{site_packages}/fastmcp/../fastmcp-3.2.4.dist-info/WHEEL",
            "fastmcp/../fastmcp-3.2.4.dist-info",
        ),
        (
            f"{site_packages}/fastmcp/../fastmcp-3.2.4.dist-info/entry_points.txt",
            "fastmcp/../fastmcp-3.2.4.dist-info",
        ),
        (
            f"{site_packages}/fastmcp/../fastmcp-3.2.4.dist-info/licenses/LICENSE",
            "fastmcp/../fastmcp-3.2.4.dist-info/licenses",
        ),
        (
            "src/bugpilot/CHANGELOG.md",
            "bugpilot",
        ),
        ("src/bugpilot/agents/default/agent.yaml", "bugpilot/agents/default"),
        ("src/bugpilot/agents/default/coder.yaml", "bugpilot/agents/default"),
        ("src/bugpilot/agents/default/explore.yaml", "bugpilot/agents/default"),
        ("src/bugpilot/agents/default/plan.yaml", "bugpilot/agents/default"),
        ("src/bugpilot/agents/default/system.md", "bugpilot/agents/default"),
        ("src/bugpilot/agents/okabe/agent.yaml", "bugpilot/agents/okabe"),
        ("src/bugpilot/prompts/compact.md", "bugpilot/prompts"),
        ("src/bugpilot/prompts/init.md", "bugpilot/prompts"),
        (
            "src/bugpilot/skills/bugpilot-help/SKILL.md",
            "bugpilot/skills/bugpilot-help",
        ),
        (
            "src/bugpilot/skills/skill-creator/SKILL.md",
            "bugpilot/skills/skill-creator",
        ),
        ("src/bugpilot/tools/agent/description.md", "bugpilot/tools/agent"),
        ("src/bugpilot/tools/ask_user/description.md", "bugpilot/tools/ask_user"),
        (
            "src/bugpilot/tools/dmail/dmail.md",
            "bugpilot/tools/dmail",
        ),
        ("src/bugpilot/tools/background/list.md", "bugpilot/tools/background"),
        ("src/bugpilot/tools/background/output.md", "bugpilot/tools/background"),
        ("src/bugpilot/tools/background/stop.md", "bugpilot/tools/background"),
        (
            "src/bugpilot/tools/file/glob.md",
            "bugpilot/tools/file",
        ),
        (
            "src/bugpilot/tools/file/grep.md",
            "bugpilot/tools/file",
        ),
        (
            "src/bugpilot/tools/file/read.md",
            "bugpilot/tools/file",
        ),
        (
            "src/bugpilot/tools/file/read_media.md",
            "bugpilot/tools/file",
        ),
        (
            "src/bugpilot/tools/file/replace.md",
            "bugpilot/tools/file",
        ),
        (
            "src/bugpilot/tools/file/write.md",
            "bugpilot/tools/file",
        ),
        ("src/bugpilot/tools/plan/description.md", "bugpilot/tools/plan"),
        ("src/bugpilot/tools/plan/enter_description.md", "bugpilot/tools/plan"),
        ("src/bugpilot/tools/shell/bash.md", "bugpilot/tools/shell"),
        (
            "src/bugpilot/tools/think/think.md",
            "bugpilot/tools/think",
        ),
        (
            "src/bugpilot/tools/todo/set_todo_list.md",
            "bugpilot/tools/todo",
        ),
        (
            "src/bugpilot/tools/web/fetch.md",
            "bugpilot/tools/web",
        ),
        (
            "src/bugpilot/tools/web/search.md",
            "bugpilot/tools/web",
        ),
    ]
    if has_rg_binary:
        expected_datas.append((f"src/bugpilot/deps/bin/{rg_binary}", "bugpilot/deps/bin"))

    assert sorted(datas) == sorted(expected_datas)


def test_pyinstaller_hiddenimports():
    from bugpilot.utils.pyinstaller import hiddenimports

    assert sorted(hiddenimports) == snapshot(
        [
            "bugpilot._build_info",
            "bugpilot.cli.export",
            "bugpilot.cli.info",
            "bugpilot.cli.mcp",
            "bugpilot.cli.plugin", "bugpilot.tools",
            "bugpilot.tools.agent",
            "bugpilot.tools.ask_user",
            "bugpilot.tools.background",
            "bugpilot.tools.display",
            "bugpilot.tools.dmail",
            "bugpilot.tools.file",
            "bugpilot.tools.file.glob",
            "bugpilot.tools.file.grep_local",
            "bugpilot.tools.file.plan_mode",
            "bugpilot.tools.file.read",
            "bugpilot.tools.file.read_media",
            "bugpilot.tools.file.replace",
            "bugpilot.tools.file.utils",
            "bugpilot.tools.file.write",
            "bugpilot.tools.plan",
            "bugpilot.tools.plan.enter",
            "bugpilot.tools.plan.heroes",
            "bugpilot.tools.shell",
            "bugpilot.tools.test",
            "bugpilot.tools.think",
            "bugpilot.tools.todo",
            "bugpilot.tools.utils", "setproctitle",
        ]
    )


def test_pyinstaller_hiddenimports_include_lazy_cli_subcommands():
    from bugpilot.cli._lazy_group import LazySubcommandGroup
    from bugpilot.utils.pyinstaller import hiddenimports

    expected_hiddenimports = {
        module_name
        for module_name, _attribute_name, _help_text in LazySubcommandGroup.lazy_subcommands.values()
    }

    assert expected_hiddenimports <= set(hiddenimports)
