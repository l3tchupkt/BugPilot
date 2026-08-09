from bugpilot.ui.shell.slash import registry

if False:
    from bugpilot.ui.shell import Shell


@registry.command
def reload(app: "Shell", args: str):
    """Reload configuration"""
    from bugpilot.cli import Reload

    raise Reload
