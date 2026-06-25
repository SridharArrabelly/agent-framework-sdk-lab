"""Section: Create a GitHub Copilot Agent.

Reference: https://devblogs.microsoft.com/agent-framework/build-ai-agents-with-github-copilot-sdk-and-microsoft-agent-framework/
"""
import asyncio

from agent_framework.github import GitHubCopilotAgent


async def main() -> None:
    agent = GitHubCopilotAgent(
        default_options={
            "model": "auto",
            "instructions": "You are a helpful assistant.",
        },
    )

    async with agent:
        result = await agent.run("What is Microsoft Agent Framework?")
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
