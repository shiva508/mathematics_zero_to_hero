"""Challenge 1 - the coordinator using specialists AS TOOLS.

In the Core lab the specialists were sub_agents: the coordinator could
*transfer* control to them. Here they are wrapped in AgentTool and used
as tools instead - the coordinator *calls* a specialist and gets the
result back, staying in charge of the conversation itself.

Complete the section marked "# YOUR CODE HERE", then run:

    uv run adk run tool_support_team

Compare the behavior with support_team: with tools, the coordinator
stays the single voice to the user.
"""

import os
from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from specialists import make_billing_agent, make_tech_agent

# YOUR CODE HERE - Challenge 1
# Build the coordinator and assign it to root_agent. This time give it
# the specialists as TOOLS, not sub_agents:
#   - wrap each specialist in AgentTool(agent=...)
#   - put both AgentTool objects in the `tools` list
#   - instruction: tell it to call the billing tool for billing
#     questions and the tech tool for technical questions, then answer
#     the user itself using the tool's result.
root_agent = LlmAgent(
    name="support_coordinator",
    model=os.getenv("ADK_MODEL", "ollama_chat/llama3.2:3b"),
    description="Answers customer questions using specialist tools.",
    instruction=("You are a customer-support coordinator. For billing, payment, "
        "and account questions, call the billing_agent tool. For technical "
        "and service-status questions, call the tech_agent tool. Then "
        "answer the user yourself using the tool's result - you remain the "
        "single voice to the customer."
        ),
    tools=[
        AgentTool(agent=make_billing_agent()),
        AgentTool(agent=make_tech_agent()),
    ]
)
