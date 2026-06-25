"""Section: Connect MCP Servers.

Reference: https://devblogs.microsoft.com/agent-framework/build-ai-agents-with-github-copilot-sdk-and-microsoft-agent-framework/
"""
import asyncio

from agent_framework.github import GitHubCopilotAgent
from copilot import MCPServerConfig, PermissionRequest, PermissionRequestResult
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
    mcp_servers: dict[str, MCPServerConfig] = {
        "filesystem": {
            "type": "stdio",
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-filesystem", "."],
            "tools": ["*"],
        },
        "microsoft-learn": {
            "type": "http",
            "url": "https://learn.microsoft.com/api/mcp",
            "tools": ["*"],
        },
    }

    agent = GitHubCopilotAgent(
        instructions="You are a helpful assistant with access to the filesystem and Microsoft Learn.",
        default_options={
            "on_permission_request": prompt_permission,
            # MCP cold start can exceed the default 60s; give servers room to spin up.
            "timeout": 300,
            "mcp_servers": mcp_servers,
        },
    )

    async with agent:
        result = await agent.run("Search Microsoft Learn for 'Azure Functions' and summarize the top result")
        print(result)


if __name__ == "__main__":
    asyncio.run(main())
