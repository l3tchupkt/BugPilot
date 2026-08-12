# Bugpilot CLI - Agent Knowledge Base

## Overview
Bugpilot CLI is an AI-powered autonomous penetration testing command-line interface. It merges the capabilities of multiple LLM providers (including Gemini, Claude, Groq, OpenAI, and local models via Ollama) with built-in security knowledge tools (like CVE database and OWASP lookups). It supports interactive ("Forge") and autonomous ("Hacker") operational modes, with a rich terminal UI, dynamic session management, and robust status handling.

## Architecture & Structure
The project follows a modular, hybrid execution architecture combining standard regex-based command parsing with an LLM-driven reasoning loop. 

### Key Components
- **`bugpilot/agent/`**: The brain of the autonomous behaviors. Includes `controller.py` (orchestrates LLMs), `executor.py` (runs commands/tools), and `intent_detector.py` (interprets user goals).
- **`bugpilot/modes/`**: Contains the logic for the two primary states:
  - `hacker.py`: Autonomous mode (`Hacker Mode`) designed for sequential, goal-oriented penetration testing and analysis.
  - `forge.py`: Interactive mode (`Forge Mode / Normal`) designed for standard Q&A and manual analysis with file context.
- **`bugpilot/tools/`**: Built-in capabilities available to the user and agent, including `security_knowledge.py` (CVE and OWASP integration), Model Context Protocol (`mcp.py`), and tool orchestration (`manager.py`).
- **`bugpilot/cli/`**: Handles user-facing slash commands (e.g., `/cve`, `/owasp`, `/update`, `/mode`, `/settings`).
- **`bugpilot/core/`**: Application scaffolding, including configuration management (`config/`), Terminal UI and theming (`terminal_ui.py`, `status_bar.py`), state persistence (`state/`), and LLM factories (`llm/`).

## Agent Execution Flow
As an AI or agent interacting with this codebase, you should be aware of the following execution flow:
1. **Input Handling:** User inputs are processed in `__main__.py`. Commands starting with `/` are routed to the `CommandHandler` (`cli/handlers.py`).
2. **Context Expansion:** The CLI natively supports `@filepath` syntax. If a user types `@README.md`, the contents of `README.md` are dynamically injected into the prompt before hitting the LLM.
3. **Intent and Reasoning:** The system uses a dual-model strategy where an *Intent LLM* detects the required actions or tools, and a *Reasoning LLM* generates the final response or drives the loop (configured in `agent/controller.py`).
4. **Safety & Execution:** Executions are wrapped in safety shims. The configuration supports blocking dangerous terminal commands.

## Contribution Guidelines for AI Agents
- **LLM Integration:** When modifying the LLM integration or adding new providers, see `bugpilot/core/llm/` for how different providers are instantiated using the factory pattern.
- **Commands:** When adding a new slash command, update the `CommandHandler` inside the `bugpilot/cli` module.
- **Security Tools:** When extending security tools (like exploit search), add the logic to `bugpilot/tools/` and expose the interface to `bugpilot/tools/manager.py` to ensure the agent can use it during Hacker mode.
- **Config Management:** Configuration relies on `PyYAML` and user-specific settings. Check `bugpilot/core/config/` for validation and schema details.

## Setup Requirements
- Python 3.8+
- UI Dependencies: `rich`, `prompt_toolkit`
- AI Dependencies: `google-generativeai`, `anthropic`, `groq`
- Run using: `python -m bugpilot`

## License
MIT License.
