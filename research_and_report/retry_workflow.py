"""Challenge 2 - recover from a failing node with a retry configuration.

The flaky_fetch node fails the first time it runs. Without a retry
configuration the whole workflow fails. Add a RetryConfig so the node
is retried after its induced failure and the workflow recovers.

This workflow uses only function nodes - it runs with no model calls.

Complete the marked section, then run:

    uv run challenge2_retry.py
"""

from google.adk.agents.context import Context
from google.adk.workflow import RetryConfig, START, Workflow, node

# Tracks attempts so the node fails once, then succeeds (an induced failure).
_attempts = {"count": 0}

async def flaky_fetch(node_input, ctx: Context):
    """A node that fails on its first attempt, then succeeds."""
    _attempts["count"] += 1
    if _attempts["count"] < 2:
        raise RuntimeError(f"induced failure on attempt {_attempts['count']}")
    return f"fetch succeeded on attempt {_attempts['count']}"


async def report(node_input, ctx: Context):
    """Terminal node - reports what the fetch produced."""
    return f"workflow finished: {node_input}"


# YOUR CODE HERE - Challenge 2
# Wrap flaky_fetch in a node WITH a retry configuration, so the node is
# retried after its induced failure instead of failing the workflow.
# Pass a retry_config argument to node():
#     retry_config=RetryConfig(max_attempts=3)
fetch_node = node(flaky_fetch, name="fetch", retry_config=RetryConfig(max_attempts=3))
report_node = node(report, name="report")
edge_list = [
                (START, fetch_node),
                (fetch_node, report_node)
            ]
retry_workflow = Workflow(name="retry_workflow",edges=edge_list)