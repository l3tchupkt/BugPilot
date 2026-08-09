# CLI Loading Time

## `src/bugpilot/__init__.py` be empty

**Scope**

`src/bugpilot/__init__.py`

**Requirements**

The `src/bugpilot/__init__.py` file must be empty, containing no code or imports.

## No unnecessary import in `src/bugpilot/cli.py`

**Scope**

`src/bugpilot/cli.py`

**Requirements**

The `src/bugpilot/cli.py` file must not import any modules from `bugpilot` or `kosong`, except for `bugpilot.constant`, at the top level.

## As-needed imports in `src/bugpilot/app.py`

**Scope**

`src/bugpilot/app.py`

**Requirements**

The `src/bugpilot/app.py` file must not import any modules prefixed with `bugpilot.ui` at the top level; instead, UI-specific modules should be imported within functions as needed.

<examples>

```python
# top-level
from bugpilot.ui.shell import ShellApp  # Incorrect: top-level import of UI module

# inside function
async def run_shell_app(...):
    from bugpilot.ui.shell import ShellApp  # Correct: import as needed
    app = ShellApp(...)
    await app.run()
```

</examples>

## `--help` should run fast

**Scope**

No specific source file.

**Requirements**

The time taken to run `uv run kimi --help` must be less than 150 milliseconds on average over 5 runs after a 3-run warm-up.
