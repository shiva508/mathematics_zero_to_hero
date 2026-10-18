"""Core Lab - a support coordinator with two specialist sub-agents.

The coordinator delegates each question to the right specialist:
billing questions to billing_agent, technical questions to tech_agent.

Complete the section marked "# YOUR CODE HERE", then run:

    uv run adk run support_team

Ask a billing question and a technical question, and watch the
coordinator hand each one to a different sub-agent.
"""

import os
from google.adk.agents import LlmAgent

from specialists import make_billing_agent, make_tech_agent

# YOUR CODE HERE - Step 1
# Build the coordinator and assign it to root_agent. It is an LlmAgent:
#   - name="support_coordinator"
#   - model=MODEL
#   - sub_agents: a fresh billing agent and a fresh tech agent, from
#     make_billing_agent() and make_tech_agent()
#   - instruction: tell it to hand billing and account questions to
#     billing_agent, and technical and service questions to tech_agent,
#     and not to answer specialist questions itself.
root_agent = LlmAgent(
    name="support_coordinator",
    model=os.getenv("ADK_MODEL", "ollama_chat/llama3.2:3b"),
    description="Routes customer questions to the right specialist.",
    instruction=("You are a customer-support coordinator. Hand billing, payment, "
        "and account questions to billing_agent. Hand technical and "
        "service-status questions to tech_agent. Do not answer specialist "
        "questions yourself - always delegate."),
    sub_agents=[make_billing_agent(), make_tech_agent()]
)

