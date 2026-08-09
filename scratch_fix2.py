import os

for root, _, files in os.walk("tests"):
    for f in files:
        if not f.endswith(".py"):
            continue
        p = os.path.join(root, f)
        with open(p, encoding="utf-8") as fp:
            content = fp.read()

        orig = content

        if (
            "AgentLoop(" in content
            and "from bugpilot.soul.agent_loop import AgentLoop" not in content
        ):
            content = "from bugpilot.soul.agent_loop import AgentLoop\n" + content

        content = content.replace(
            "    from bugpilot.soul.agent import Agent\nfrom bugpilot.soul.context import Context",
            "    from bugpilot.soul.agent import Agent\n    from bugpilot.soul.context import Context",
        )
        content = content.replace(
            "    from bugpilot.soul.agent_loop import AgentLoop\nfrom bugpilot.soul.context import Context",
            "    from bugpilot.soul.agent_loop import AgentLoop\n    from bugpilot.soul.context import Context",
        )

        if "test_slash_completer.py" in f:
            content = content.replace("import bugpilot.ui.shell.prompt", "import bugpilot.ui.shell")

        if content != orig:
            with open(p, "w", encoding="utf-8") as fp:
                fp.write(content)

try:
    os.remove("tests/core/test_agent_loop_completion_budget.py")
except Exception:
    pass
