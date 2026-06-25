# copilot-sdk-lab

Hands-on Python examples for building AI agents with the **GitHub Copilot SDK** and the **Microsoft Agent Framework**.

Each script in [examples/](examples/) maps 1:1 to a section of the dev blog post that inspired this lab:

> [Build AI Agents with GitHub Copilot SDK and Microsoft Agent Framework](https://devblogs.microsoft.com/agent-framework/build-ai-agents-with-github-copilot-sdk-and-microsoft-agent-framework/) by Dmytro Struk, Microsoft Agent Framework dev blog.

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) for env + dependency management
- Node.js + `npm` (the GitHub Copilot CLI ships as an npm package)
- A GitHub account with Copilot access

Install the GitHub Copilot CLI once and sign in:

```pwsh
npm install -g @github/copilot
copilot auth login   # device-flow login
```

> The `agent-framework-github-copilot` Python package shells out to this CLI executable. VS Code's bundled Copilot is **not** the same CLI.

## Setup

```pwsh
uv sync
```

The lock pins `agent-framework==1.9.0` and `agent-framework-github-copilot>=1.0.0rc1`. Pre-releases are allowed via `[tool.uv] prerelease = "allow"`.

For the multi-agent workflow example, copy `.env.example` to `.env`, fill in your Azure OpenAI endpoint + chat model, then `az login`:

```pwsh
Copy-Item .env.example .env
# edit .env
az login
```

## Examples

Run any example with `uv run python examples\<file>.py`.

### 1. Basic agent - [examples/01_basic_agent.py](examples/01_basic_agent.py)
Create a `GitHubCopilotAgent`, ask one question, print the answer. The minimum viable agent.

### 2. Function tools - [examples/02_function_tools.py](examples/02_function_tools.py)
Extend the agent with a typed Python function (`get_weather`). The framework converts the annotated signature into a tool definition the model can call.

### 3. Streaming - [examples/03_streaming.py](examples/03_streaming.py)
Stream the response token-by-token with `agent.run(prompt, stream=True)` instead of waiting for the full result.

### 4. Multi-turn conversation - [examples/04_multi_turn.py](examples/04_multi_turn.py)
Use `agent.create_session()` and pass `session=...` on each `run()` call so the agent remembers earlier turns (it should recall "Alice" on the second prompt).

### 5. Permissions - [examples/05_permissions.py](examples/05_permissions.py)
The agent cannot run shell commands, touch files, or fetch URLs unless you approve. Wire `on_permission_request` to an interactive prompt that returns `PermissionDecisionApproveOnce()` or `PermissionDecisionDeniedInteractivelyByUser()` (both from `copilot.generated.rpc`).

### 6. MCP servers - [examples/06_mcp_servers.py](examples/06_mcp_servers.py)
Attach a local stdio MCP server (`@modelcontextprotocol/server-filesystem`) and a remote HTTP server (`https://learn.microsoft.com/api/mcp`). The default 60s timeout is bumped to 300s so cold starts do not fail.

### 7. Multi-agent workflow - [examples/07_multi_agent_workflow.py](examples/07_multi_agent_workflow.py)
Compose two agents in a sequential workflow: an **Azure OpenAI** writer drafts a tagline, then a **GitHub Copilot** reviewer critiques it. Streaming chunks are buffered per executor and flushed on `executor_completed`, so output is one clean block per agent. Requires `.env` + `az login`.

## Notes from the lab

A few things that bit while wiring these up against the current SDK versions:

- `agent.run(prompt, stream=True)` is the streaming entry point on `GitHubCopilotAgent` - there is no `run_stream`.
- Multi-turn uses `agent.create_session()` + `session=...`, not `get_new_thread()` / `thread=...`.
- Permission types live at the **top level** of `copilot` (`PermissionRequest`, `MCPServerConfig`); the concrete decision classes are in `copilot.generated.rpc`. `PermissionRequest` is a dataclass, so use `getattr(request, "kind", ...)` instead of `.get()`.
- `agent_framework.openai.OpenAIChatClient` is the unified client. When `AZURE_OPENAI_ENDPOINT` is set and a `credential` is supplied, it operates in Azure OpenAI mode. There is no separate `AzureOpenAIChatClient`.
- For the multi-agent workflow, `Workflow.run(prompt, stream=True)` emits one `output` event per streamed chunk (with `event.data.text`) and one `executor_completed` event per agent. Group chunks by `executor_id` and flush on completion.

## Reference

- Dev blog: [Build AI Agents with GitHub Copilot SDK and Microsoft Agent Framework](https://devblogs.microsoft.com/agent-framework/build-ai-agents-with-github-copilot-sdk-and-microsoft-agent-framework/)
- [GitHub Copilot SDK](https://github.com/github/copilot-sdk)
- [Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
- [Agent Framework getting-started tutorials](https://learn.microsoft.com/agent-framework/tutorials/overview)

## License

Released under the [MIT License](LICENSE).
