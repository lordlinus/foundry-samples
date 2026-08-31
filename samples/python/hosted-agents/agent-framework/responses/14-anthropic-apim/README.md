# Anthropic via APIM Hosted Agent (Responses Protocol)

An [Agent Framework](https://github.com/microsoft/agent-framework) agent hosted on Microsoft Foundry that talks to an **Anthropic (Claude) model through an Azure API Management (APIM) gateway**, using the **Responses protocol**.

## Why this sample exists

`FoundryChatClient` (used by [01-basic](../01-basic)) speaks the OpenAI Responses protocol to a Foundry-deployed model. Claude models exposed through Azure AI Foundry / APIM are **Anthropic Messages-protocol only** — there is no OpenAI-compatible route — so `FoundryChatClient` cannot reach them. This sample uses `AnthropicFoundryClient` from the [`agent-framework-anthropic`](https://pypi.org/project/agent-framework-anthropic/) package instead, pointed at an APIM gateway that fronts one or more Anthropic backends.

## How it works

See [main.py](src/agent-framework-agent-anthropic-apim/main.py). `AnthropicFoundryClient(model=..., base_url=..., api_key=...)` sends the standard Anthropic SDK `x-api-key` header, which APIM can map to whatever header/auth scheme the upstream Anthropic backend expects. The agent is still served via `ResponsesHostServer`, so Foundry's hosted-agent session, conversation, and history management (`agent_session_id`, `previous_response_id`) work exactly as they do for Foundry-deployed models — swapping the chat client does not change how sessions/state are managed, because that is owned by the hosting layer, not the chat client.

## Prerequisites

1. An APIM gateway with an API that proxies `POST /v1/messages` to an Anthropic-compatible backend (Anthropic's own API, or Claude models deployed on Azure AI Foundry), forwarding the caller's subscription key as `x-api-key` (and defaulting `anthropic-version` if the backend requires it).
2. The gateway's base URL up to (not including) `/v1/messages`, e.g. `https://<apim-name>.azure-api.net/anthropic`.
3. A subscription key authorized for that API.

## Option 1: Azure Developer CLI (`azd`)

### Prerequisites

1. **Azure Developer CLI (`azd`)** — [Install azd](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/install-azd)
2. Install the AI agent extension:
   ```bash
   azd ext install microsoft.foundry
   ```
3. Authenticate:
   ```bash
   azd auth login
   ```

### Initialize the agent project

```bash
mkdir my-anthropic-apim-agent && cd my-anthropic-apim-agent

azd ai agent init -m https://github.com/microsoft-foundry/foundry-samples/blob/main/samples/python/hosted-agents/agent-framework/responses/14-anthropic-apim/azure.yaml
```

### Configure the APIM connection

```bash
azd env set ANTHROPIC_MODEL_NAME claude-sonnet-5
azd env set APIM_ANTHROPIC_BASE_URL https://<apim-name>.azure-api.net/anthropic
azd env set APIM_SUBSCRIPTION_KEY <your-apim-subscription-key>
```

### Provision Azure resources (if needed)

```bash
azd provision
```

### Run the agent locally

```bash
azd ai agent run
```

### Invoke the local agent

```bash
azd ai agent invoke --local "Say hello and tell me which model you are."
```

### Deploy to Foundry

```bash
azd deploy
```

### Invoke the deployed agent

```bash
azd ai agent invoke "Say hello and tell me which model you are."
```

## Option 2: VS Code (Foundry Toolkit)

Same as [01-basic](../01-basic#option-2-vs-code-foundry-toolkit), but set `ANTHROPIC_MODEL_NAME`, `APIM_ANTHROPIC_BASE_URL`, and `APIM_SUBSCRIPTION_KEY` in your local `.env` (see [.env.example](src/agent-framework-agent-anthropic-apim/.env.example)) before pressing **F5** or running `python main.py`.

## Next steps

- [Basic Hosted Agent](../01-basic) — the OpenAI/Foundry-model equivalent of this sample
- [Manage hosted agents](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/manage-hosted-agent) — monitor and manage deployed agents
