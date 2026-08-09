from __future__ import annotations


class BugPilotError(Exception):
    """Base exception class for BugPilot."""

    pass


class ConfigError(BugPilotError, ValueError):
    """Configuration error."""

    pass


class AgentSpecError(BugPilotError, ValueError):
    """Agent specification error."""

    pass


class InvalidToolError(BugPilotError, ValueError):
    """Invalid tool error."""

    pass


class SystemPromptTemplateError(BugPilotError, ValueError):
    """System prompt template error."""

    pass


class MCPConfigError(BugPilotError, ValueError):
    """MCP config error."""

    pass


class MCPRuntimeError(BugPilotError, RuntimeError):
    """MCP runtime error."""

    pass
