# Config Overrides

BugPilot configuration can be set through multiple methods, with different sources overriding each other by priority.

## Priority

Configuration priority from highest to lowest:

1. **Environment variables** - Highest priority, for temporary overrides or CI/CD environments
2. **CLI flags** - Flags specified at startup
3. **Configuration file** - `~/.bugpilot/config.toml` or file specified via `--config-file`

## CLI flags

### Configuration file related

| Flag | Description |
| --- | --- |
| `--config <TOML/JSON>` | Pass configuration content directly, overrides default config file |
| `--config-file <PATH>` | Specify configuration file path, replaces default `~/.bugpilot/config.toml` |

`--config` and `--config-file` cannot be used together.

### Model related

| Flag | Description |
| --- | --- |
| `--model, -m <NAME>` | Specify model name to use |

The model specified by `--model` must be defined in the configuration file's `models`. If not specified, uses `default_model` from the configuration file.

### Behavior related

| Flag | Description |
| --- | --- |
| `--thinking` | Enable thinking mode |
| `--no-thinking` | Disable thinking mode |
| `--yolo, --yes, -y` | Auto-approve all tool calls (user still reachable for `AskUserQuestion`) |
| `--afk` | Away-from-keyboard: auto-approve all tool calls and auto-dismiss `AskUserQuestion` |
| `--plan` | Start in plan mode |

`--thinking` / `--no-thinking` overrides the thinking state saved from the last session. If not specified, uses the last session's state.

`--plan` enables plan mode for new sessions; when resuming an existing session, it forces plan mode on. You can also set `default_plan_mode = true` in the config file to start new sessions in plan mode by default.

## Environment variable overrides

Environment variables can override provider and model settings without modifying the configuration file. This is particularly useful in the following scenarios:

- Injecting keys in CI/CD environments
- Temporarily testing different API endpoints
- Switching between multiple environments

Environment variables take effect based on the current provider type:

- `bugpilot` type providers: Use `BUGPILOT_*` environment variables
- `openai_legacy` or `openai_responses` type providers: Use `OPENAI_*` environment variables
- Other provider types: Environment variable overrides not supported

See [Environment Variables](./env-vars.md) for the complete list.

Example:

```sh
BUGPILOT_API_KEY="sk-xxx" BUGPILOT_MODEL_NAME="bugpilot-k2-thinking-turbo" bugpilot
```

## Configuration priority example

Assume the configuration file `~/.bugpilot/config.toml` contains:

```toml
default_model = "bugpilot-for-coding"

[providers.bugpilot-for-coding]
type = "bugpilot"
base_url = "https://api.bugpilot.com/coding/v1"
api_key = "sk-config"

[models.bugpilot-for-coding]
provider = "bugpilot-for-coding"
model = "bugpilot-for-coding"
max_context_size = 262144
```

Here are the configuration sources in different scenarios:

| Scenario | `base_url` | `api_key` | `model` |
| --- | --- | --- | --- |
| `bugpilot` | Config file | Config file | Config file |
| `BUGPILOT_API_KEY=sk-env bugpilot` | Config file | Environment variable | Config file |
| `bugpilot --model other` | Config file | Config file | CLI flag |
| `BUGPILOT_MODEL_NAME=k2 bugpilot` | Config file | Config file | Environment variable |
