"""Challenge 1 - branch the workflow on the type of request.

A router function node inspects the request and routes it to either a
quick-summary path or a full-report path. The router is a function node,
so the decision is deterministic and costs no model call.

Complete classify_request where marked, then run:

    uv run challenge1_routing.py
"""

import asyncio
import os

from dotenv import load_dotenv
from google.adk.agents.context import Context
from google.adk.workflow import START, Workflow, node
from agents import summarizer,reporter

load_dotenv()


async def classify_request(node_input, ctx: Context):
    """Router: send summary requests one way, report requests the other."""
    # YOUR CODE HERE - Challenge 1
    # 1. Read the request text - node_input.parts[0].text - lowercased.
    # 2. If it mentions "summary" or "summarize", set ctx.route = "summary".
    # 3. Otherwise set ctx.route = "report".
    # The routing map below sends the run to the matching node.
    text = node_input.parts[0].text.lower() if node_input.parts else ""
    print(f"Text: {text}")
    if "summary" in text or "summarize" in text:
        ctx.route = "summary"
    else:
        ctx.route = "report"
    return f"routed to '{ctx.route}'"


router_node = node(classify_request, name="router")
summary_node = node(summarizer, name="summarizer")
report_node = node(reporter, name="reporter")
edge_list = [
        (START, router_node),
        (router_node, {"summary": summary_node, "report": report_node}),
    ]

router_workflow = Workflow(name="request_router",edges=edge_list)