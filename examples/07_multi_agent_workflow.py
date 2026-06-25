"""Section: Use GitHub Copilot in a Multi-Agent Workflow.

Reference: https://devblogs.microsoft.com/agent-framework/build-ai-agents-with-github-copilot-sdk-and-microsoft-agent-framework/

An Azure OpenAI agent drafts a marketing tagline; a GitHub Copilot agent
reviews it. We buffer streaming chunks per executor and print one clean block
per agent.
"""
import asyncio
from collections import defaultdict

from dotenv import load_dotenv
from agent_framework import WorkflowBuilder
from agent_framework.github import GitHubCopilotAgent
from agent_framework.openai import OpenAIChatClient
from azure.identity import AzureCliCredential

load_dotenv()


async def main() -> None:
    chat_client = OpenAIChatClient(credential=AzureCliCredential())
    writer = chat_client.as_agent(
        instructions="You are a concise copywriter. Provide a single, punchy marketing sentence based on the prompt.",
        name="writer",
    )

    reviewer = GitHubCopilotAgent(
        instructions="You are a thoughtful reviewer. Give brief feedback on the previous assistant message.",
        name="reviewer",
    )

    workflow = (
        WorkflowBuilder(start_executor=writer)
        .add_chain([writer, reviewer])
        .build()
    )

    buffers: dict[str, list[str]] = defaultdict(list)

    async with reviewer:
        async for event in workflow.run(
            "Write a tagline for a budget-friendly electric bike.", stream=True
        ):
            executor_id = getattr(event, "executor_id", None)
            if event.type == "output" and executor_id:
                chunk = getattr(event.data, "text", "") or ""
                if chunk:
                    buffers[executor_id].append(chunk)
            elif event.type == "executor_completed" and executor_id in buffers:
                text = "".join(buffers.pop(executor_id)).strip()
                if text:
                    print(f"[{executor_id}]: {text}\n")


if __name__ == "__main__":
    asyncio.run(main())
