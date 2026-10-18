"""Core Lab - Retry and fallback for low-confidence results.

The classifier sometimes returns a result it is not confident about.
Complete document_classifier_retry.py() so it re-runs the agent when confidence
is below the threshold and falls back to a safe default when retries
are exhausted.

Run from the files/ directory:

    uv run document_classifier_retry.py
"""

import asyncio
import json

from dotenv import load_dotenv
from google.adk.runners import InMemoryRunner
from google.genai import types

from doc_classifier.agent import root_agent
from document_store import DOCUMENTS_METADATA

load_dotenv()
APP_NAME = "doc_classifier_retry"
USER_ID = "student"
CONFIDENCE_THRESHOLD = 0.7
MAX_ATTEMPTS = 3

async def common_classifier(runner: InMemoryRunner, text: str, attempt:int) -> dict:
    """Run the classifier once and return the result as a dict."""
    session_id = f"session-{attempt}-{abs(hash(text)) % 100000}"
    initial_session = await runner.session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=session_id)
    #print(f"Session created: {initial_session}")
    message = types.Content(role="user", parts=[types.Part(text=text)])
    async for _event in runner.run_async(user_id=USER_ID, session_id=session_id, new_message=message):
        pass
    end_session = await runner.session_service.get_session(app_name=APP_NAME, user_id=USER_ID, session_id=session_id)
    #print(f"Session retrieved: {end_session}")
    result = end_session.state.get("classification")
    if isinstance(result, str):
        result = json.loads(result)
    return result or {}


async def classify_with_retry(runner: InMemoryRunner, text:str) ->dict:
    """Classify a document, retrying when confidence is low.

        YOUR CODE HERE - Step 4
        Run the classifier up to MAX_ATTEMPTS times with run_once(). Return
        the first result whose "confidence" is at least CONFIDENCE_THRESHOLD.
        If no attempt clears the threshold, return a fallback dict with
        category "unknown", confidence 0.0, and a summary that explains the
        classification was not confident.
    """
    for attempt in range(1, MAX_ATTEMPTS + 1):
        result = await common_classifier(runner, text, attempt)
        confidence = result.get("confidence", 0.0)
        if confidence >= CONFIDENCE_THRESHOLD:
            return result
    return {
            "category": "unknown",
            "confidence": 0.0,
            "summary": (
                "Classification did not reach the confidence threshold "
                f"after {MAX_ATTEMPTS} attempts."
            ),
        }

async def main() -> None:
    runner = InMemoryRunner(agent=root_agent, app_name=APP_NAME)
    for doc_id, text in DOCUMENTS_METADATA.items():
        result = await classify_with_retry(runner, text)
        print(f"{doc_id}: {result}")


if __name__ == "__main__":
    asyncio.run(main())