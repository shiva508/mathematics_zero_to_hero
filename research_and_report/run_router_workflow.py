"""Challenge 1 - branch the workflow on the type of request.

A router function node inspects the request and routes it to either a
quick-summary path or a full-report path. The router is a function node,
so the decision is deterministic and costs no model call.

Complete classify_request where marked, then run:

    uv run challenge1_routing.py
"""

import asyncio
from google.adk.runners import InMemoryRunner
from google.genai import errors as genai_errors
from google.genai import types
from router_workflow import router_workflow

REQUESTS = [
    "Give me a quick summary of quantum computing.",
    "I need a detailed report on quantum computing.",
]

async def router_workerflow_runner():
    runner = InMemoryRunner(node=router_workflow, app_name="request_router")
    for request in REQUESTS:
        init_session = await runner.session_service.create_session(app_name="request_router", user_id="student")
        query = types.Content(role="user", parts=[types.Part(text=request)])
        print(f"\nRequest: {request}")
        try:
            async for _event in runner.run_async(user_id="student", session_id=init_session.id, new_message=query):
                info = getattr(_event, "node_info", None)
                output = getattr(_event, "output", None)
                if info and output is not None:
                    print(f" [node] {info.path}")
                    print(f" [output]: {output}")
                if _event.is_final_response() and _event.content and  _event.content.parts:
                    print(f"Result { _event.content.parts[0].text}")

        except genai_errors.APIError as exc:
            code = getattr(exc, "code", None)
            if code == 429:
                print("  [the Gemini API quota was exceeded - use a billing-enabled key]")
            else:
                print("  [the model is temporarily unavailable - run again]")


if __name__ == "__main__":
    asyncio.run(router_workerflow_runner())