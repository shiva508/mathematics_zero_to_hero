"""Challenge 2 - recover from a failing node with a retry configuration.

The flaky_fetch node fails the first time it runs. Without a retry
configuration the whole workflow fails. Add a RetryConfig so the node
is retried after its induced failure and the workflow recovers.

This workflow uses only function nodes - it runs with no model calls.

Complete the marked section, then run:

    uv run challenge2_retry.py
"""

import asyncio
from google.adk.runners import InMemoryRunner
from google.genai import types
from retry_workflow import retry_workflow


async def retry_workflow_runner():
    runner =  InMemoryRunner(node=retry_workflow, app_name="retry_workflow")
    init_session = await runner.session_service.create_session(app_name="retry_workflow", user_id="student")
    message = types.Content(role="user", parts=[types.Part(text="go")])
    print("Running the workflow (the fetch node fails on its first attempt)...\n")
    try:
        async for _event in runner.run_async(user_id="student", session_id=init_session.id, new_message=message):
            info = getattr(_event, "node_info", None)
            output = getattr(_event, "output", None)
            if info and output is not None:
                print(f"[node] {info.path}: {output}")
            if _event.is_final_response() and _event.content and _event.content.parts:
                print(f"Result {_event.content.parts[0].text}")
        print("\nThe workflow completed - the retry recovered the failed node.")
    except Exception as exc:  # noqa: BLE001 - demo: show the unrecovered failure
        print(f"\nThe workflow failed: {exc!r}")
        print("Add a RetryConfig to the fetch node so it recovers.")



if __name__ == "__main__":
    asyncio.run(retry_workflow_runner())