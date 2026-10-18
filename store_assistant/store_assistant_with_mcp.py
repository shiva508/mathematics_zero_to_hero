"""Challenge 2 - Connect an external tool through MCP.

mcp_server.py is a small Model Context Protocol server that exposes a
shipping-estimate tool. Complete the McpToolset so this agent can launch
that server and use its tool.

Run from the files/ directory:

    uv run challenge2_mcp.py
"""

import asyncio
import os
import sys

from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.adk.runners import InMemoryRunner
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import (
    StdioConnectionParams,
)
from google.genai import types
from mcp import StdioServerParameters

load_dotenv()

APP_NAME = "store_mcp_assistant"
USER_ID = "student"

# YOUR CODE HERE - Challenge 2
# Build an McpToolset that launches mcp_server.py over stdio and assign
# it to shipping_toolset. Use:
#   connection_params=StdioConnectionParams(
#       server_params=StdioServerParameters(
#           command=sys.executable, args=["mcp_server.py"]))
#   tool_filter=["get_shipping_estimate"]
shipping_toolset = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command=sys.executable, args=["store_mcp_server.py"]
        )
    ),
    tool_filter=["get_shipping_estimate"],
)


mcp_root_agent = LlmAgent(
    name="shipping_assistant",
    model=os.getenv("ADK_MODEL", "ollama_chat/llama3.2:3b"),
    description="Answers shipping cost and delivery questions.",
    instruction=(
        "You help customers estimate shipping. Use the "
        "get_shipping_estimate tool to answer shipping questions."
    ),
    tools=[shipping_toolset] if shipping_toolset else [],
)

async def run_shipping_query()->None:
    runner = InMemoryRunner(agent=mcp_root_agent, app_name=APP_NAME)
    init_session = await runner.session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id="session-1")
    query = types.Content(role="user", parts=[types.Part(text="How much to ship a 3 kg package to the UK?")])
    async for event in runner.run_async(user_id=USER_ID, session_id="session-1", new_message=query):
        if event.is_final_response() and event.content and event.content.parts:
            print(event.content.parts[0].text)



if __name__ == "__main__":
    asyncio.run(run_shipping_query())


