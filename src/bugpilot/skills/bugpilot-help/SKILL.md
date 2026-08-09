---
name: bugpilot-help
description: Answer BugPilot usage, configuration, and troubleshooting questions. Use when user asks about BugPilot installation, setup, configuration, slash commands, keyboard shortcuts, MCP integration, providers, environment variables, how something works internally, or any questions about BugPilot itself.
---

# BugPilot Help

Help users with BugPilot questions by consulting documentation and source code.

## Strategy

1. **Prefer official documentation** for most questions
2. **Read local source** when in bugpilot project itself, or when user is developing with bugpilot as a library (e.g., importing from `bugpilot` in their code)
3. **Clone and explore source** for complex internals not covered in docs - **ask user for confirmation first**

## Documentation

Base URL: `https://l3tchupkt.github.io/bugpilot/`

Fetch documentation index to find relevant pages:

```
https://l3tchupkt.github.io/bugpilot/llms.txt
```

### Page URL Pattern

- English: `https://l3tchupkt.github.io/bugpilot/en/...`
- Chinese: `https://l3tchupkt.github.io/bugpilot/zh/...`

### Topic Mapping

| Topic | Page |
|-------|------|
| Installation, first run | `/en/guides/getting-started.md` |
| Config files | `/en/configuration/config-files.md` |
| Providers, models | `/en/configuration/providers.md` |
| Environment variables | `/en/configuration/env-vars.md` |
| Slash commands | `/en/reference/slash-commands.md` |
| CLI flags | `/en/reference/bugpilot-command.md` |
| Keyboard shortcuts | `/en/reference/keyboard.md` |
| MCP | `/en/customization/mcp.md` |
| Agents | `/en/customization/agents.md` |
| Skills | `/en/customization/skills.md` |
| FAQ | `/en/faq.md` |

## Source Code

Repository: `https://github.com/l3tchupkt/bugpilot`

When to read source:

- In bugpilot project directory (check `pyproject.toml` for `name = "bugpilot"`)
- User is importing `bugpilot` as a library in their project
- Question about internals not covered in docs (ask user before cloning)
