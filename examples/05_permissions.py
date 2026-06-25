"""Section: Enable Permissions.

Reference: https://devblogs.microsoft.com/agent-framework/build-ai-agents-with-github-copilot-sdk-and-microsoft-agent-framework/
"""
import asyncio

from agent_framework.github import GitHubCopilotAgent
from copilot import PermissionRequest, PermissionRequestResult
from copilot.generated.rpc import (
    PermissionDecisionApproveOnce,
    PermissionDecisionDeniedInteractivelyByUser,
)


def prompt_permission(
    request: PermissionRequest, context: dict[str, str]
) -> PermissionRequestResult:
    kind = getattr(request, "kind", "unknown")
    print(f"\n[Permission Request: {kind}]")

    response = input("Approve? (y/n): ").strip().lower()
    if response in ("y", "yes"):
        return PermissionDecisionApproveOnce()
    return PermissionDecisionDeniedInteractivelyByUser()


async def main() -> None:
    agent = GitHubCopilotAgent(
        instructions="You are a helpful assistant that can execute shell commands.",
        default_options={
            "on_permission_request": prompt_permission,
        },
    )

    async with agent:
        result = await agent.run("List the Python files in the current directory")
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
