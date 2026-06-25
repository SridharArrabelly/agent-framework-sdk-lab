# agent-framework-sdk-lab

A personal learning lab for the **Microsoft Agent Framework**, working through the dev blog series that pairs the framework with provider-specific agent SDKs (GitHub Copilot, Claude, ...).

Each provider lives in its own folder. The files inside follow the same numbered structure so the same concept (basic agent, function tools, streaming, multi-turn, permissions, MCP, multi-agent workflow) lines up across providers and you can compare APIs side-by-side.

## Why this repo exists

The Microsoft Agent Framework dev blog has been publishing a series of "Build AI Agents with `<SDK>` and Microsoft Agent Framework" posts. Each post walks the same 7 capabilities through a different vendor SDK. This repo is me reading those posts, running every snippet against the current package versions, fixing what no longer matches the published code, and keeping the working result around as a reference.

The intent is **comparative learning**, not a polished sample gallery: each folder is a faithful adaptation of one blog post, with notes on what the SDK actually does today vs. what the post describes.

## Roadmap

| Provider | Folder | Source post | Status |
| --- | --- | --- | --- |
| GitHub Copilot SDK | [copilot/](copilot/) | [Build AI Agents with GitHub Copilot SDK and Microsoft Agent Framework](https://devblogs.microsoft.com/agent-framework/build-ai-agents-with-github-copilot-sdk-and-microsoft-agent-framework/) | Done |
| Claude Agent SDK | `claude/` | [Build AI Agents with Claude Agent SDK and Microsoft Agent Framework](https://devblogs.microsoft.com/agent-framework/build-ai-agents-with-claude-agent-sdk-and-microsoft-agent-framework/) | Planned |
| Future posts in the series | per-folder | TBD | As they ship |

## Repo layout

```
agent-framework-sdk-lab/
  copilot/              # GitHub Copilot SDK examples (01..07)
  claude/               # (planned) Claude Agent SDK examples
  .env.example          # provider-specific env vars (currently Azure OpenAI for copilot/07)
  pyproject.toml        # uv-managed deps for every provider in this repo
  README.md             # this file
  LICENSE
```

A single `pyproject.toml` + `uv.lock` covers all providers so `uv sync` once gives you everything.

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) for env + dependency management
- Provider-specific tooling listed in each provider folder below (e.g. GitHub Copilot CLI, Anthropic API key)

```pwsh
uv sync
```

## Providers

### GitHub Copilot SDK -> [copilot/](copilot/)

Adapts [Build AI Agents with GitHub Copilot SDK and Microsoft Agent Framework](https://devblogs.microsoft.com/agent-framework/build-ai-agents-with-github-copilot-sdk-and-microsoft-agent-framework/) by Dmytro Struk.

**Extra prerequisites**

- Node.js + `npm` (the GitHub Copilot CLI ships as an npm package)
- A GitHub account with Copilot access

```pwsh
npm install -g @github/copilot
copilot auth login   # device-flow login
```

> The `agent-framework-github-copilot` Python package shells out to this CLI executable. VS Code's bundled Copilot is **not** the same CLI.

For the multi-agent workflow example only, copy `.env.example` to `.env`, fill in your Azure OpenAI endpoint + chat model, then `az login`:

```pwsh
Copy-Item .env.example .env
# edit .env
az login
```

**Examples** (run with `uv run python copilot\<file>.py`)

1. Basic agent - [copilot/01_basic_agent.py](copilot/01_basic_agent.py) - create a `GitHubCopilotAgent`, ask one question, print the answer.
2. Function tools - [copilot/02_function_tools.py](copilot/02_function_tools.py) - extend the agent with a typed Python function (`get_weather`).
3. Streaming - [copilot/03_streaming.py](copilot/03_streaming.py) - stream the response token-by-token with `agent.run(prompt, stream=True)`.
4. Multi-turn conversation - [copilot/04_multi_turn.py](copilot/04_multi_turn.py) - use `agent.create_session()` so the agent remembers earlier turns.
5. Permissions - [copilot/05_permissions.py](copilot/05_permissions.py) - approve/deny shell, file, and URL access via `on_permission_request`.
6. MCP servers - [copilot/06_mcp_servers.py](copilot/06_mcp_servers.py) - attach a local stdio MCP server and a remote HTTP server (Microsoft Learn).
7. Multi-agent workflow - [copilot/07_multi_agent_workflow.py](copilot/07_multi_agent_workflow.py) - Azure OpenAI writer + GitHub Copilot reviewer in a sequential workflow, with per-executor stream buffering.

**Notes from the lab**

- `agent.run(prompt, stream=True)` is the streaming entry point on `GitHubCopilotAgent` - there is no `run_stream`.
- Multi-turn uses `agent.create_session()` + `session=...`, not `get_new_thread()` / `thread=...`.
- Permission types live at the **top level** of `copilot` (`PermissionRequest`, `MCPServerConfig`); the concrete decision classes are in `copilot.generated.rpc`. `PermissionRequest` is a dataclass, so use `getattr(request, "kind", ...)` instead of `.get()`.
- `agent_framework.openai.OpenAIChatClient` is the unified client. When `AZURE_OPENAI_ENDPOINT` is set and a `credential` is supplied, it operates in Azure OpenAI mode. There is no separate `AzureOpenAIChatClient`.
- For the multi-agent workflow, `Workflow.run(prompt, stream=True)` emits one `output` event per streamed chunk (with `event.data.text`) and one `executor_completed` event per agent. Group chunks by `executor_id` and flush on completion.

### Claude Agent SDK -> `claude/` (planned)

Will adapt [Build AI Agents with Claude Agent SDK and Microsoft Agent Framework](https://devblogs.microsoft.com/agent-framework/build-ai-agents-with-claude-agent-sdk-and-microsoft-agent-framework/) once worked through. Same numbered structure (`01_basic_agent.py` ... `07_multi_agent_workflow.py`) so it lines up with `copilot/`.

## Reference

- [Microsoft Agent Framework dev blog](https://devblogs.microsoft.com/agent-framework/)
- [Microsoft Agent Framework on GitHub](https://github.com/microsoft/agent-framework)
- [Agent Framework getting-started tutorials](https://learn.microsoft.com/agent-framework/tutorials/overview)
- [GitHub Copilot SDK](https://github.com/github/copilot-sdk)

## License

Released under the [MIT License](LICENSE).
