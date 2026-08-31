# Copyright (c) Microsoft. All rights reserved.

import os

from agent_framework import Agent
from agent_framework_anthropic import AnthropicFoundryClient
from agent_framework_foundry_hosting import ResponsesHostServer
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def main():
    model_name = os.getenv("ANTHROPIC_MODEL_NAME")
    apim_base_url = os.getenv("APIM_ANTHROPIC_BASE_URL")
    apim_key = os.getenv("APIM_SUBSCRIPTION_KEY")
    if not model_name or not apim_base_url or not apim_key:
        raise RuntimeError(
            "Anthropic-via-APIM is not configured. Set ANTHROPIC_MODEL_NAME, "
            "APIM_ANTHROPIC_BASE_URL and APIM_SUBSCRIPTION_KEY."
        )

    # Routes Anthropic Messages traffic through the APIM gateway instead of a
    # Foundry-deployed model: base_url is the gateway's anthropic API base
    # (e.g. https://<apim>.azure-api.net/anthropic) and api_key is sent as the
    # x-api-key header APIM expects.
    client = AnthropicFoundryClient(
        model=model_name,
        base_url=apim_base_url,
        api_key=apim_key,
    )

    agent = Agent(
        client=client,
        instructions="You are a friendly assistant. Keep your answers brief.",
    )

    server = ResponsesHostServer(agent)
    server.run()


if __name__ == "__main__":
    main()
