# BugPilot

[![Commit Activity](https://img.shields.io/github/commit-activity/w/l3tchupkt/bugpilot)](https://github.com/l3tchupkt/bugpilot/graphs/commit-activity)
[![Checks](https://img.shields.io/github/check-runs/l3tchupkt/bugpilot/main)](https://github.com/l3tchupkt/bugpilot/actions)
[![Version](https://img.shields.io/pypi/v/bugpilot)](https://pypi.org/project/bugpilot/)

BugPilot is a AI security research and  penetration testing CLI agent. It helps you automate vulnerability discovery, analyze codebases for security flaws, and orchestrate security tooling directly from your terminal.

## Getting Started

### Installation

```sh
pip install bugpilot
```

### Usage

```sh
bugpilot
```

## Features

- **Agentic Security Workflows**: BugPilot autonomously explores environments and investigates vulnerabilities.
- **Local-First Configuration**: Run everything from your terminal using local configuration files and environment overrides.
- **Provider Agnostic**: Connect BugPilot to your preferred LLM provider via standard configuration.
- **Extensible Tools**: Supports MCP (Model Context Protocol) to seamlessly plug in custom vulnerability scanners and external APIs.

## Development

To develop BugPilot, run:

```sh
git clone https://github.com/l3tchupkt/bugpilot.git
cd bugpilot

make prepare  # prepare the development environment
```

Refer to the following commands after you make changes:

```sh
uv run bugpilot  # run BugPilot CLI
make format      # format code
make check       # run linting and type checking
make test        # run tests
```
