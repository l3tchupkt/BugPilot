# `bugpilot term` Subcommand

The `bugpilot term` command launches the [Toad](https://github.com/batrachianai/toad) terminal UI, a modern terminal interface built with [Textual](https://textual.textualize.io/).

```sh
bugpilot term [OPTIONS]
```

## Description

[Toad](https://github.com/batrachianai/toad) is a graphical terminal interface for BugPilot that communicates with the BugPilot backend via the ACP protocol. It provides a richer interactive experience with better output rendering and layout.

When you run `bugpilot term`, it automatically starts a `bugpilot acp` server in the background, and Toad connects to it as an ACP client.

## Options

All extra options are passed through to the internal `bugpilot acp` command. For example:

```sh
bugpilot term --work-dir /path/to/project --model bugpilot-k2
```

Common options:

| Option | Description |
|--------|-------------|
| `--work-dir PATH` | Specify working directory |
| `--model NAME` | Specify model |
| `--yolo` | Auto-approve all tool calls |

For the full list of options, see [`bugpilot` command](./bugpilot-command.md).

## System requirements

::: warning Note
`bugpilot term` requires Python 3.14+. If you installed BugPilot with an older Python version, you need to reinstall with Python 3.14:

```sh
uv tool install --python 3.14 bugpilot
```
:::
