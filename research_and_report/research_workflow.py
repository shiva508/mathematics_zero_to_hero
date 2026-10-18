"""Core Lab - a research-and-report workflow graph.

The workflow:

    START -> planner -> (background_researcher, news_researcher)
          -> research_join -> writer -> review_router
          -> "revise" back to writer, or "done" to finalize

That single graph uses every pattern from the module: a sequential
chain, a parallel fan-out with a join, a routed cycle (the revise
loop), and conditional routing.

Complete the two sections marked "# YOUR CODE HERE", then run:

    uv run run_workflow.py
"""

from google.adk.agents.context import Context
from google.adk.workflow import JoinNode, START, Workflow, node

from agents import (
    background_researcher,
    news_researcher,
    planner,
    writer,
)

# The revise loop runs the writer this many times before finalizing.
MAX_REVISIONS = 2


async def finalize(node_input, ctx: Context) -> dict:
    """Terminal node: returns the finished report from session state."""
    return {"report": ctx.state.get("draft", "")}


async def review_router(node_input, ctx: Context):
    """Decides whether the draft needs another revision pass.

    This is a function node - a deterministic step with no model call.
    """
    # YOUR CODE HERE - Step 1
    # 1. Read the revision count with ctx.state.get("revision_round", 0)
    #    and add 1.
    # 2. Write the new count back to ctx.state["revision_round"].
    # 3. If the count has reached MAX_REVISIONS, set ctx.route = "done";
    #    otherwise set ctx.route = "revise". The routing map in `edges`
    #    sends the run to the node matching that value.
    # 4. Return a short status string.
    rounds = ctx.state.get("revision_round", 0) + 1
    ctx.state["revision_round"] = rounds
    ctx.route = "done" if rounds >= MAX_REVISIONS else "revise"
    return f"revision check: round {rounds}, route '{ctx.route}'"


# --- Nodes (provided) -------------------------------------------------
# Each node object must be created once and reused in the edges list.
planner_node = node(planner, name="planner")
background_node = node(background_researcher, name="background_researcher")
news_node = node(news_researcher, name="news_researcher")
research_join = JoinNode(name="research_join")
writer_node = node(writer, name="writer")
review_node = node(review_router, name="review_router")
finalize_node = node(finalize, name="finalize")


# --- Edges ------------------------------------------------------------
# YOUR CODE HERE - Step 2
# Build the edges list that wires the graph. Each edge is a tuple:
#   (START, planner_node)
#   (planner_node, (background_node, news_node))   # tuple = fan-out
#   ((background_node, news_node), research_join)  # tuple = fan-in
#   (research_join, writer_node)
#   (writer_node, review_node)
#   (review_node, {"revise": writer_node, "done": finalize_node})
edges = [
    (START, planner_node),
    (planner_node, (background_node, news_node)),
    ((background_node, news_node), research_join),
    (research_join, writer_node),
    (writer_node, review_node),
    (review_node, {"revise": writer_node, "done": finalize_node}),
]


workflow = Workflow(name="research_workflow", edges=edges)
