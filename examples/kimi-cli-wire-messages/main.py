import asyncio

from kaos.path import KaosPath
from bugpilot.app import BugPilotCLI, enable_logging
from bugpilot.session import Session
from rich import print


async def main():
    enable_logging()
    session = await Session.create(KaosPath.cwd())
    instance = await BugPilotCLI.create(session)
    user_input = "Hello!"

    async for msg in instance.run(
        user_input=user_input,
        cancel_event=asyncio.Event(),
        merge_wire_messages=True,
    ):
        print(msg)

    # print the last assistant message
    print(instance.soul.context.history[-1])


if __name__ == "__main__":
    asyncio.run(main())
