# BugPilot SDK

BugPilot SDK provides a convenient way to access the BugPilot API and build agent workflows in Python.

## Installation

BugPilot SDK requires Python 3.12 or higher. We recommend using uv as the package manager.

```bash
uv init --python 3.12  # or higher
```

Then add BugPilot SDK as a dependency:

```bash
uv add bugpilot-sdk
```

## Examples

### Simple chat completion

```python
import asyncio

from bugpilot_sdk import BugPilot, Message, generate


async def main() -> None:
    kimi = BugPilot(
        base_url="https://api.moonshot.ai/v1",
        api_key="your_kimi_api_key_here",
        model="kimi-k2-turbo-preview",
    )

    history = [
        Message(role="user", content="Who are you?"),
    ]

    result = await generate(
        chat_provider=kimi,
        system_prompt="You are a helpful assistant.",
        tools=[],
        history=history,
    )
    print(result.message)
    print(result.usage)


asyncio.run(main())
```

### Streaming output

```python
import asyncio

from bugpilot_sdk import BugPilot, Message, StreamedMessagePart, generate


async def main() -> None:
    kimi = BugPilot(
        base_url="https://api.moonshot.ai/v1",
        api_key="your_kimi_api_key_here",
        model="kimi-k2-turbo-preview",
    )

    history = [
        Message(role="user", content="Who are you?"),
    ]

    def output(message_part: StreamedMessagePart) -> None:
        print(message_part)

    result = await generate(
        chat_provider=kimi,
        system_prompt="You are a helpful assistant.",
        tools=[],
        history=history,
        on_message_part=output,
    )
    print(result.message)
    print(result.usage)


asyncio.run(main())
```

### Upload video

```python
import asyncio
from pathlib import Path
from bugpilot_sdk import BugPilot, Message, TextPart, generate


async def main() -> None:
    kimi = BugPilot(
        base_url="https://api.moonshot.ai/v1",
        api_key="your_kimi_api_key_here",
        model="kimi-k2-turbo-preview",
    )

    video_path = Path("demo.mp4")
    video_part = await kimi.files.upload_video(
        data=video_path.read_bytes(),
        mime_type="video/mp4",
    )

    history = [
        Message(
            role="user",
            content=[
                TextPart(text="Please describe this video."),
                video_part,
            ],
        ),
    ]

    result = await generate(
        chat_provider=kimi,
        system_prompt="You are a helpful assistant.",
        tools=[],
        history=history,
    )
    print(result.message)
    print(result.usage)


asyncio.run(main())
```

### Tool calling with `step`

```python
import asyncio

from pydantic import BaseModel

from bugpilot_sdk import CallableTool2, BugPilot, Message, SimpleToolset, StepResult, ToolOk, ToolReturnValue, step


class AddToolParams(BaseModel):
    a: int
    b: int


class AddTool(CallableTool2[AddToolParams]):
    name: str = "add"
    description: str = "Add two integers."
    params: type[AddToolParams] = AddToolParams

    async def __call__(self, params: AddToolParams) -> ToolReturnValue:
        return ToolOk(output=str(params.a + params.b))


async def main() -> None:
    kimi = BugPilot(
        base_url="https://api.moonshot.ai/v1",
        api_key="your_kimi_api_key_here",
        model="kimi-k2-turbo-preview",
    )

    toolset = SimpleToolset()
    toolset += AddTool()

    history = [
        Message(role="user", content="Please add 2 and 3 with the add tool."),
    ]

    result: StepResult = await step(
        chat_provider=kimi,
        system_prompt="You are a precise math tutor.",
        toolset=toolset,
        history=history,
    )
    print(result.message)
    print(await result.tool_results())


asyncio.run(main())
```

## Environment variables

- `BUGPILOT_API_KEY`: API key for the BugPilot API.
- `BUGPILOT_BASE_URL`: Override the API base URL (defaults to `https://api.moonshot.ai/v1`).
