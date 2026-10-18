"""Core Lab - the coordinator with the tech agent running REMOTELY.

This coordinator is identical to support_team's, except the tech
specialist is no longer a local sub-agent. It is a RemoteA2aAgent - a
proxy for the agent served by a2a_server.py over the network.

Start a2a_server.py first (in its own terminal), then complete the
section marked "# YOUR CODE HERE" and run:

    uv run adk run remote_support_team
"""

import os

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from specialists import make_billing_agent

# The A2A server (a2a_server.py) publishes its agent card here.
TECH_AGENT_CARD_URL = "http://localhost:8001/.well-known/agent-card.json"

MODEL = Gemini(
    model=os.getenv("ADK_MODEL", "gemini-3.5-flash"),
    retry_options=types.HttpRetryOptions(
        attempts=6,
        initial_delay=2.0,
        max_delay=60.0,
        exp_base=2.0,
        jitter=1.0,
        http_status_codes=[408, 429, 500, 502, 503, 504],
    ),
)


def ensure_transfer_mode(agent: RemoteA2aAgent) -> RemoteA2aAgent:
    """Compatibility shim for ADK versions where RemoteA2aAgent lacks mode."""
    if not hasattr(agent, "mode"):
        object.__setattr__(agent, "mode", "default")
    return agent

# YOUR CODE HERE - Step 4
# 1. Build a RemoteA2aAgent named "tech_agent". Pass:
#       agent_card=TECH_AGENT_CARD_URL
#       description="Remote technical-support specialist."
#    Then wrap it with ensure_transfer_mode(...).
# 2. Build the coordinator (LlmAgent named "support_coordinator", same
#    instruction as in support_team) with sub_agents set to a fresh
#    billing agent and the RemoteA2aAgent. Assign it to root_agent.
remote_tech_agent =  ensure_transfer_mode(
    RemoteA2aAgent(
        name="tech_agent",
        description="Remote technical-support specialist.",
        agent_card=TECH_AGENT_CARD_URL
    )
)

root_agent = LlmAgent(
    name="support_coordinator",
    model=os.getenv("ADK_MODEL", "ollama_chat/llama3.2:3b"),
    description="Routes customer questions to the right specialist.",
    instruction=(
        "You are a customer-support coordinator. Hand billing, payment, "
        "and account questions to billing_agent. Hand technical and "
        "service-status questions to tech_agent. Do not answer specialist "
        "questions yourself - always delegate."
    ),
    sub_agents=[make_billing_agent(), remote_tech_agent],
)