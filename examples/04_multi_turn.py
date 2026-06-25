"""Section: Multi-Turn Conversations.

Reference: https://devblogs.microsoft.com/agent-framework/build-ai-agents-with-github-copilot-sdk-and-microsoft-agent-framework/
"""
import asyncio

from agent_framework.github import GitHubCopilotAgent


async def main() -> None:
    agent = GitHubCopilotAgent(
        default_options={"instructions": "You are a helpful assistant."},
    )

    async with agent:
        session = agent.create_session()

        result1 = await agent.run("My name is Alice.", session=session)
        print(f"Agent: {result1}")

        result2 = await agent.run("What's my name?", session=session)
        print(f"Agent: {result2}")


if __name__ == "__main__":
    asyncio.run(main())
