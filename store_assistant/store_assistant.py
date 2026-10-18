"""Run the store assistant over a few sample questions.

This file is provided complete - you do not need to edit it. Run it from
the lab's files/ directory:

    uv run ask_assistant.py

To watch the tool calls step by step in the Dev UI instead, run:

    uv run adk web
"""

import asyncio

from dotenv import load_dotenv
from google.adk.runners import InMemoryRunner
from google.genai import errors as genai_errors
from google.genai import types

from agent import store_assistant_agent

load_dotenv()

APP_NAME = "store_assistant_demo"
USER_ID = "student"


async def run_query(runner: InMemoryRunner, question: str, base_session_id: str, max_attempts: int = 3) -> str:
    """Run one question and return the agent's answer.

    Calls to the Gemini API can fail for two reasons this helper handles:
    a temporary 503 when the service is busy (retried with a short,
    growing delay) and a 429 quota error (reported with a clear message).
    """
    message = types.Content(role="user", parts=[types.Part(text=question)])
    for attempt in range(1, max_attempts + 1):
        unique_session_id = f"{base_session_id}-attempt-{max_attempts}"
        init_session = await runner.session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=unique_session_id)
        try:
            answer = ""
            async for _event in runner.run_async(user_id=USER_ID, session_id=unique_session_id, new_message=message):
                if _event.is_final_response() and _event.content and _event.content.parts:
                    answer = _event.content.parts[0].text or ""
            return answer
        except genai_errors.APIError as exc:
            code = getattr(exc, "code", None)
            if code == 429:
                return (
                        "[the Gemini API quota was exceeded - a free-tier key "
                        "allows only a few requests per day; ask your "
                        "instructor for a billing-enabled API key]"
                    )
            if code is None or code < 500:
                raise
            if attempt == max_attempts:
                    return (
                        "[the model is temporarily unavailable - "
                        "please run the script again in a moment]"
                    )
            await asyncio.sleep(2 * attempt)
    return ""

async def main():
    runner = InMemoryRunner(agent=store_assistant_agent, app_name=APP_NAME)
    questions = [
        "What is the status of order ORD-001?",
        "Do you have any mechanical keyboards in stock?",
        "Is the usb-c cable available right now?",
        "What is the status of order ORD-999?",
    ]
    for i, question in enumerate(questions):
        answer = await run_query(runner, question, base_session_id=f"question_{i}")
        print(f"Q: {question}\nA: {answer}\n")


if __name__ == "__main__":
    asyncio.run(main())