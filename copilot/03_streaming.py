"""Section: Stream Responses.

Reference: https://devblogs.microsoft.com/agent-framework/build-ai-agents-with-github-copilot-sdk-and-microsoft-agent-framework/
"""
import asyncio

from agent_framework.github import GitHubCopilotAgent


async def main() -> None:
    agent = GitHubCopilotAgent(
        default_options={"instructions": "You are a helpful assistant."},
    )

    async with agent:
        print("Agent: ", end="", flush=True)
        async for chunk in agent.run("Tell me a short story.", stream=True):
            if chunk.text:
                print(chunk.text, end="", flush=True)
        print()


if __name__ == "__main__":
    asyncio.run(main())
