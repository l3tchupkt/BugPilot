# Changelog

All notable changes to BugPilot will be documented in this file.

## [Unreleased] - BugPilot v1.4.0 (Upcoming)

### 🚀 Features & Enhancements
- **Dynamic Model Autocomplete:** Added intelligent, real-time fetching of available models directly from AI provider APIs (OpenAI, NVIDIA, Anthropic, etc.) natively inside the `/model` dropdown.
- **Top-Level Settings CLI:** Completely eliminated nested and interactive TUI configurations. Settings are now fully inline using lightning-fast top-level commands (`/connect`, `/model`, `/theme`, `/output`).
- **Command History Navigation:** Integrated persistent prompt sessions, allowing users to scroll through their command history using the Up and Down arrow keys just like a standard terminal.
- **Dynamic Agent Re-Initialization:** Encapsulated agent initialization logic within the core CLI to support hot-swapping providers and API keys without needing to restart the application.
- **Asynchronous Execution & Dynamic Context:** Upgraded the execution engine to handle long-running operations asynchronously without locking the UI, paired with real-time dynamic context management.
- **Multi-Agent Swarm Framework:** Laid the foundational groundwork for a multi-agent orchestration architecture to handle complex parallel tasks.
- **Docker Containerization:** Added Docker support for sandboxed and reproducible environments.
- **Agent To-Do Tool:** Deployed a persistent memory `task.md` tool for agents to track multi-step goals, drastically improving long-term task completion.

### 🐛 Bug Fixes
- **Startup Crash Resiliency:** Fixed a critical bug where missing API keys on startup would crash the application or freeze the prompt. The CLI now gracefully falls back and prompts you to use `/connect` when ready.
- **LLM Adapter Reliability:** Patched cascading errors in the LLM factory logic and exposed the internal `chat_provider` to prevent crashes in the main agent loop.
- **Unlimited Context Meter:** Removed arbitrary token limits from the status bar, reflecting the new scalable continuous memory architecture.

### 🧹 Chores & Cleanup
- **Codebase De-bloat:** Scanned and purged legacy unused files (`workflow_manager.py`, `filesystem.py`, `logic_engine.py`) resulting in a leaner, faster repository.
- **Testing:** Added new unit tests for autocomplete caching and UI elements, boosting overall coverage.

## [1.3.4] - 2026-08-11
- **Documentation Overhaul:** Rewrote the README.md to a professional production standard, detailing features, architecture, and roadmaps.
- **Security Enhancements:** Added a comprehensive `SECURITY.md` advisory policy.
- **Slash Command Autocomplete:** Introduced the initial `/` slash command autocompleter, paving the way for the current streamlined CLI experience.
