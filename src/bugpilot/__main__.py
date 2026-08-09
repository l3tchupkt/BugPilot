from __future__ import annotations

import sys
from collections.abc import Sequence
from pathlib import Path


def _prog_name() -> str:
    return Path(sys.argv[0]).name or "bugpilot"


def main(argv: Sequence[str] | None = None) -> int | str | None:
    from bugpilot.utils.proxy import normalize_proxy_env

    # Install excepthook before anything else so startup-phase crashes are captured.
    #     install_crash_handlers()
    normalize_proxy_env()

    args = list(sys.argv[1:] if argv is None else argv)

    if len(args) == 1 and args[0] in {"--version", "-V"}:
        from bugpilot.constant import get_version

        print(f"bugpilot, version {get_version()}")
        return 0

    from bugpilot.cli import cli
    from bugpilot.utils.environment import GitBashNotFoundError

    try:
        return cli(args=args, prog_name=_prog_name())
    except SystemExit as exc:
        return exc.code
    except GitBashNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    finally:
        pass


if __name__ == "__main__":
    raise SystemExit(main())
