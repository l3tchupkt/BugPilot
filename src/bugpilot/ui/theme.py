"""Centralized terminal color theme definitions.

All UI-facing colors live here so that switching between dark and light
terminal themes only requires changing the active ``ThemeName``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from prompt_toolkit.styles import Style as PTKStyle
from rich.style import Style as RichStyle

type ThemeName = Literal["dark", "light", "hacker", "cyberpunk", "retro"]


# ---------------------------------------------------------------------------
# Diff colors (used by utils/rich/diff_render.py)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class DiffColors:
    add_bg: RichStyle
    del_bg: RichStyle
    add_hl: RichStyle
    del_hl: RichStyle


_DIFF_DARK = DiffColors(
    add_bg=RichStyle(bgcolor="#12261e"),
    del_bg=RichStyle(bgcolor="#2d1214"),
    add_hl=RichStyle(bgcolor="#1a4a2e"),
    del_hl=RichStyle(bgcolor="#5c1a1d"),
)

_DIFF_LIGHT = DiffColors(
    add_bg=RichStyle(bgcolor="#dafbe1"),
    del_bg=RichStyle(bgcolor="#ffebe9"),
    add_hl=RichStyle(bgcolor="#aff5b4"),
    del_hl=RichStyle(bgcolor="#ffc1c0"),
)
_DIFF_HACKER = DiffColors(
    add_bg=RichStyle(bgcolor="#003300"),
    del_bg=RichStyle(bgcolor="#330000"),
    add_hl=RichStyle(bgcolor="#004400"),
    del_hl=RichStyle(bgcolor="#440000"),
)

_DIFF_CYBERPUNK = DiffColors(
    add_bg=RichStyle(bgcolor="#2c003e"),
    del_bg=RichStyle(bgcolor="#3d0014"),
    add_hl=RichStyle(bgcolor="#470066"),
    del_hl=RichStyle(bgcolor="#660022"),
)

_DIFF_RETRO = DiffColors(
    add_bg=RichStyle(bgcolor="#332211"),
    del_bg=RichStyle(bgcolor="#331111"),
    add_hl=RichStyle(bgcolor="#443311"),
    del_hl=RichStyle(bgcolor="#441111"),
)



# ---------------------------------------------------------------------------
# Task browser colors (used by ui/shell/task_browser.py)
# ---------------------------------------------------------------------------


def _task_browser_style_dark() -> PTKStyle:
    return PTKStyle.from_dict(
        {
            "header": "bg:#1f2937 #e5e7eb",
            "header.title": "bg:#1f2937 #67e8f9 bold",
            "header.meta": "bg:#1f2937 #9ca3af",
            "status.running": "bg:#1f2937 #86efac bold",
            "status.success": "bg:#1f2937 #86efac",
            "status.warning": "bg:#1f2937 #fbbf24",
            "status.error": "bg:#1f2937 #fca5a5",
            "status.info": "bg:#1f2937 #93c5fd",
            "task-list": "bg:#111827 #d1d5db",
            "task-list.checked": "bg:#164e63 #ecfeff bold",
            "frame.border": "#155e75",
            "frame.label": "bg:#0f172a #67e8f9 bold",
            "footer": "bg:#0f172a #cbd5e1",
            "footer.key": "bg:#0f172a #67e8f9 bold",
            "footer.text": "bg:#0f172a #cbd5e1",
            "footer.warning": "bg:#7f1d1d #fecaca bold",
            "footer.meta": "bg:#0f172a #94a3b8",
        }
    )


def _task_browser_style_light() -> PTKStyle:
    return PTKStyle.from_dict(
        {
            "header": "bg:#e5e7eb #1f2937",
            "header.title": "bg:#e5e7eb #0e7490 bold",
            "header.meta": "bg:#e5e7eb #6b7280",
            "status.running": "bg:#e5e7eb #166534 bold",
            "status.success": "bg:#e5e7eb #166534",
            "status.warning": "bg:#e5e7eb #92400e",
            "status.error": "bg:#e5e7eb #991b1b",
            "status.info": "bg:#e5e7eb #1e40af",
            "task-list": "bg:#f9fafb #374151",
            "task-list.checked": "bg:#cffafe #164e63 bold",
            "frame.border": "#0e7490",
            "frame.label": "bg:#f1f5f9 #0e7490 bold",
            "footer": "bg:#f1f5f9 #475569",
            "footer.key": "bg:#f1f5f9 #0e7490 bold",
            "footer.text": "bg:#f1f5f9 #475569",
            "footer.warning": "bg:#fee2e2 #991b1b bold",
            "footer.meta": "bg:#f1f5f9 #64748b",
        }
    )



def _task_browser_style_hacker() -> PTKStyle:
    return PTKStyle.from_dict({
        "header": "bg:#001100 #00ff00",
        "header.title": "bg:#001100 #00ff00 bold",
        "header.meta": "bg:#001100 #008800",
        "status.running": "bg:#001100 #00ff00 bold",
        "status.success": "bg:#001100 #00cc00",
        "status.warning": "bg:#001100 #cccc00",
        "status.error": "bg:#001100 #ff0000",
        "status.info": "bg:#001100 #00cccc",
        "task-list": "bg:#000500 #00aa00",
        "task-list.checked": "bg:#002200 #00ff00 bold",
        "frame.border": "#00ff00",
        "frame.label": "bg:#000500 #00ff00 bold",
        "footer": "bg:#000500 #00cc00",
        "footer.key": "bg:#000500 #00ff00 bold",
        "footer.text": "bg:#000500 #00cc00",
        "footer.warning": "bg:#220000 #ff0000 bold",
        "footer.meta": "bg:#000500 #008800",
    })

def _task_browser_style_cyberpunk() -> PTKStyle:
    return PTKStyle.from_dict({
        "header": "bg:#1a0b2e #ff00ff",
        "header.title": "bg:#1a0b2e #00ffff bold",
        "header.meta": "bg:#1a0b2e #ff00aa",
        "status.running": "bg:#1a0b2e #00ffcc bold",
        "status.success": "bg:#1a0b2e #00ffcc",
        "status.warning": "bg:#1a0b2e #ffcc00",
        "status.error": "bg:#1a0b2e #ff003c",
        "status.info": "bg:#1a0b2e #00ccff",
        "task-list": "bg:#0d0514 #cc00ff",
        "task-list.checked": "bg:#2e0f4c #00ffff bold",
        "frame.border": "#ff00ff",
        "frame.label": "bg:#0d0514 #00ffff bold",
        "footer": "bg:#0d0514 #ff00aa",
        "footer.key": "bg:#0d0514 #00ffff bold",
        "footer.text": "bg:#0d0514 #ff00aa",
        "footer.warning": "bg:#4c001a #ff003c bold",
        "footer.meta": "bg:#0d0514 #8800aa",
    })

def _task_browser_style_retro() -> PTKStyle:
    return PTKStyle.from_dict({
        "header": "bg:#221100 #ffaa00",
        "header.title": "bg:#221100 #ffcc00 bold",
        "header.meta": "bg:#221100 #cc8800",
        "status.running": "bg:#221100 #aaff00 bold",
        "status.success": "bg:#221100 #88cc00",
        "status.warning": "bg:#221100 #ffaa00",
        "status.error": "bg:#221100 #ff4400",
        "status.info": "bg:#221100 #00ccff",
        "task-list": "bg:#110800 #cc9900",
        "task-list.checked": "bg:#331a00 #ffcc00 bold",
        "frame.border": "#ff9900",
        "frame.label": "bg:#110800 #ffcc00 bold",
        "footer": "bg:#110800 #ccaa00",
        "footer.key": "bg:#110800 #ffcc00 bold",
        "footer.text": "bg:#110800 #ccaa00",
        "footer.warning": "bg:#441100 #ff4400 bold",
        "footer.meta": "bg:#110800 #aa6600",
    })
# ---------------------------------------------------------------------------
# Prompt / completion menu colors (used by ui/shell/prompt.py)
# ---------------------------------------------------------------------------


_PROMPT_STYLE_DARK = {
    "bottom-toolbar": "noreverse",
    "running-prompt-placeholder": "fg:#7c8594 italic",
    "running-prompt-separator": "fg:#4a5568",
    "slash-completion-menu": "",
    "slash-completion-menu.separator": "fg:#4a5568",
    "slash-completion-menu.marker": "fg:#4a5568",
    "slash-completion-menu.marker.current": "fg:#4f9fff",
    "slash-completion-menu.command": "fg:#a6adba",
    "slash-completion-menu.meta": "fg:#7c8594",
    "slash-completion-menu.command.current": "fg:#6fb7ff bold",
    "slash-completion-menu.meta.current": "fg:#56a4ff",
}

_PROMPT_STYLE_LIGHT = {
    "bottom-toolbar": "noreverse",
    "running-prompt-placeholder": "fg:#6b7280 italic",
    "running-prompt-separator": "fg:#d1d5db",
    "slash-completion-menu": "",
    "slash-completion-menu.separator": "fg:#d1d5db",
    "slash-completion-menu.marker": "fg:#9ca3af",
    "slash-completion-menu.marker.current": "fg:#2563eb",
    "slash-completion-menu.command": "fg:#4b5563",
    "slash-completion-menu.meta": "fg:#6b7280",
    "slash-completion-menu.command.current": "fg:#1d4ed8 bold",
    "slash-completion-menu.meta.current": "fg:#2563eb",
}



_PROMPT_STYLE_HACKER = {
    "bottom-toolbar": "noreverse",
    "running-prompt-placeholder": "fg:#008800 italic",
    "running-prompt-separator": "fg:#004400",
    "slash-completion-menu": "bg:#001100",
    "slash-completion-menu.separator": "fg:#004400",
    "slash-completion-menu.marker": "fg:#006600",
    "slash-completion-menu.marker.current": "fg:#00ff00",
    "slash-completion-menu.command": "fg:#00aa00",
    "slash-completion-menu.meta": "fg:#008800",
    "slash-completion-menu.command.current": "fg:#00ff00 bold",
    "slash-completion-menu.meta.current": "fg:#00cc00",
}

_PROMPT_STYLE_CYBERPUNK = {
    "bottom-toolbar": "noreverse",
    "running-prompt-placeholder": "fg:#aa00aa italic",
    "running-prompt-separator": "fg:#660066",
    "slash-completion-menu": "bg:#1a0b2e",
    "slash-completion-menu.separator": "fg:#660066",
    "slash-completion-menu.marker": "fg:#aa00aa",
    "slash-completion-menu.marker.current": "fg:#00ffff",
    "slash-completion-menu.command": "fg:#cc00ff",
    "slash-completion-menu.meta": "fg:#ff00aa",
    "slash-completion-menu.command.current": "fg:#00ffff bold",
    "slash-completion-menu.meta.current": "fg:#00ccff",
}

_PROMPT_STYLE_RETRO = {
    "bottom-toolbar": "noreverse",
    "running-prompt-placeholder": "fg:#cc8800 italic",
    "running-prompt-separator": "fg:#884400",
    "slash-completion-menu": "bg:#221100",
    "slash-completion-menu.separator": "fg:#884400",
    "slash-completion-menu.marker": "fg:#cc8800",
    "slash-completion-menu.marker.current": "fg:#ffcc00",
    "slash-completion-menu.command": "fg:#ffaa00",
    "slash-completion-menu.meta": "fg:#cc8800",
    "slash-completion-menu.command.current": "fg:#ffcc00 bold",
    "slash-completion-menu.meta.current": "fg:#ffaa00",
}
# ---------------------------------------------------------------------------
# Bottom toolbar fragment colors (used by ui/shell/prompt.py)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class ToolbarColors:
    separator: str
    yolo_label: str
    afk_label: str
    plan_label: str
    plan_prompt: str
    cwd: str
    bg_tasks: str
    tip: str


_TOOLBAR_DARK = ToolbarColors(
    separator="fg:#4d4d4d",
    yolo_label="bold fg:#ffff00",
    afk_label="bold fg:#ff8800",
    plan_label="bold fg:#00aaff",
    plan_prompt="fg:#00aaff",
    cwd="fg:#666666",
    bg_tasks="fg:#888888",
    tip="fg:#555555",
)

_TOOLBAR_LIGHT = ToolbarColors(
    separator="fg:#d1d5db",
    yolo_label="bold fg:#b45309",
    afk_label="bold fg:#c2410c",
    plan_label="bold fg:#2563eb",
    plan_prompt="fg:#2563eb",
    cwd="fg:#6b7280",
    bg_tasks="fg:#4b5563",
    tip="fg:#9ca3af",
)



_TOOLBAR_HACKER = ToolbarColors(
    separator="fg:#004400",
    yolo_label="bold fg:#ffff00",
    afk_label="bold fg:#ffaa00",
    plan_label="bold fg:#00ffff",
    plan_prompt="fg:#00ffff",
    cwd="fg:#00aa00",
    bg_tasks="fg:#008800",
    tip="fg:#006600",
)

_TOOLBAR_CYBERPUNK = ToolbarColors(
    separator="fg:#660066",
    yolo_label="bold fg:#ffcc00",
    afk_label="bold fg:#ff5500",
    plan_label="bold fg:#00ffff",
    plan_prompt="fg:#00ffff",
    cwd="fg:#cc00ff",
    bg_tasks="fg:#aa00aa",
    tip="fg:#ff00aa",
)

_TOOLBAR_RETRO = ToolbarColors(
    separator="fg:#884400",
    yolo_label="bold fg:#ff0000",
    afk_label="bold fg:#ff5500",
    plan_label="bold fg:#00ccff",
    plan_prompt="fg:#00ccff",
    cwd="fg:#cc9900",
    bg_tasks="fg:#aa8800",
    tip="fg:#cc8800",
)
# ---------------------------------------------------------------------------
# MCP status prompt colors (used by ui/shell/mcp_status.py)
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class MCPPromptColors:
    text: str
    detail: str
    connected: str
    connecting: str
    pending: str
    failed: str


_MCP_PROMPT_DARK = MCPPromptColors(
    text="fg:#d4d4d4",
    detail="fg:#7c8594",
    connected="fg:#56d364",
    connecting="fg:#56a4ff",
    pending="fg:#f2cc60",
    failed="fg:#ff7b72",
)

_MCP_PROMPT_LIGHT = MCPPromptColors(
    text="fg:#374151",
    detail="fg:#6b7280",
    connected="fg:#166534",
    connecting="fg:#1d4ed8",
    pending="fg:#92400e",
    failed="fg:#dc2626",
)



_MCP_PROMPT_HACKER = MCPPromptColors(
    text="fg:#00ff00",
    detail="fg:#00aa00",
    connected="fg:#00ff00",
    connecting="fg:#00ffff",
    pending="fg:#ffff00",
    failed="fg:#ff0000",
)

_MCP_PROMPT_CYBERPUNK = MCPPromptColors(
    text="fg:#00ffff",
    detail="fg:#cc00ff",
    connected="fg:#00ffcc",
    connecting="fg:#00ccff",
    pending="fg:#ffcc00",
    failed="fg:#ff003c",
)

_MCP_PROMPT_RETRO = MCPPromptColors(
    text="fg:#ffcc00",
    detail="fg:#cc9900",
    connected="fg:#88cc00",
    connecting="fg:#00ccff",
    pending="fg:#ffaa00",
    failed="fg:#ff4400",
)
# ---------------------------------------------------------------------------
# Public API — resolve by theme name
# ---------------------------------------------------------------------------

_active_theme: ThemeName = "dark"


def set_active_theme(theme: ThemeName) -> None:
    global _active_theme
    _active_theme = theme


def get_active_theme() -> ThemeName:
    return _active_theme



def get_diff_colors() -> DiffColors:
    return {
        "dark": _DIFF_DARK,
        "light": _DIFF_LIGHT,
        "hacker": _DIFF_HACKER,
        "cyberpunk": _DIFF_CYBERPUNK,
        "retro": _DIFF_RETRO
    }.get(_active_theme, _DIFF_DARK)


def get_task_browser_style() -> PTKStyle:
    func = {
        "dark": _task_browser_style_dark,
        "light": _task_browser_style_light,
        "hacker": _task_browser_style_hacker,
        "cyberpunk": _task_browser_style_cyberpunk,
        "retro": _task_browser_style_retro
    }.get(_active_theme, _task_browser_style_dark)
    return func()


def get_prompt_style() -> PTKStyle:
    d = {
        "dark": _PROMPT_STYLE_DARK,
        "light": _PROMPT_STYLE_LIGHT,
        "hacker": _PROMPT_STYLE_HACKER,
        "cyberpunk": _PROMPT_STYLE_CYBERPUNK,
        "retro": _PROMPT_STYLE_RETRO
    }.get(_active_theme, _PROMPT_STYLE_DARK)
    return PTKStyle.from_dict(d)


def get_toolbar_colors() -> ToolbarColors:
    return {
        "dark": _TOOLBAR_DARK,
        "light": _TOOLBAR_LIGHT,
        "hacker": _TOOLBAR_HACKER,
        "cyberpunk": _TOOLBAR_CYBERPUNK,
        "retro": _TOOLBAR_RETRO
    }.get(_active_theme, _TOOLBAR_DARK)


def get_mcp_prompt_colors() -> MCPPromptColors:
    return {
        "dark": _MCP_PROMPT_DARK,
        "light": _MCP_PROMPT_LIGHT,
        "hacker": _MCP_PROMPT_HACKER,
        "cyberpunk": _MCP_PROMPT_CYBERPUNK,
        "retro": _MCP_PROMPT_RETRO
    }.get(_active_theme, _MCP_PROMPT_DARK)
