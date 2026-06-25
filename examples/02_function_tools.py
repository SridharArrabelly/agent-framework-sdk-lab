"""Section: Add Function Tools.

Reference: https://devblogs.microsoft.com/agent-framework/build-ai-agents-with-github-copilot-sdk-and-microsoft-agent-framework/
"""
import asyncio
from typing import Annotated

from pydantic import Field

from agent_framework.github import GitHubCopilotAgent


def get_weather(
    location: Annotated[str, Field(description="The location to get the weather for.")],
) -> str:
    """Get the weather for a given location."""
    return f"The weather in {location} is sunny with a high of 25C."


async def main() -> None:
    agent = GitHubCopilotAgent(
        default_options={"instructions": "You are a helpful weather agent."},
        tools=[get_weather],
    )

    async with agent:
        result = await agent.run("What's the weather like in Seattle?")
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
