import asyncio
import json

from dotenv import load_dotenv
from google.adk.runners import InMemoryRunner
from google.genai import errors as genai_errors
from google.genai import types
from agent import root_agent
from document_store import DOCUMENTS_METADATA

load_dotenv()

APP_NAME = "doc_classifier_demo"
USER_ID = "student"

async def document_classifier(runner: InMemoryRunner,
                              doc_id: str,
                              text: str,
                              max_attempts: int = 3) -> None:
    """Classify one document and print the result.

        The Gemini API can briefly return a 503 error when it is under heavy
        load. That is temporary, so this helper retries a few times with a
        short, growing delay before giving up gracefully.
    """
    message = types.Content(role="user", parts=[types.Part(text=text)])
    for attempt in range(1, max_attempts + 1):
        session_id = f"session-{doc_id}-attempt-{attempt}"
        initial_session = await runner.session_service.create_session(
                        app_name=APP_NAME,
                        user_id=USER_ID,
                        session_id=session_id)
        #print(f"Session created: {initial_session}")
        try:
            final_response = ""
            async for event in runner.run_async(user_id=USER_ID, session_id=session_id, new_message=message):
                if event.is_final_response() and event.content and event.content.parts:
                    final_response = event.content.parts[0].text or ""
            end_session = await runner.session_service.get_session(app_name=APP_NAME, user_id=USER_ID, session_id=session_id)
            #print(f"Session retrieved: {end_session}")
            print(f"Final response: {final_response}")
            result = end_session.state.get("classification")
            print(f"Session state: {result}")
            break
        except genai_errors.APIError as exc:
            code = getattr(exc, "code", None)
            if code == 429:
                print(f"\n=== {doc_id} ===")
                print("  (the Gemini API quota was exceeded - a free-tier key allows")
                print("   only a few requests per day; use a billing-enabled API key)")
                return
            if code is None or code < 500:
                raise
            if attempt == max_attempts:
                print(f"\n=== {doc_id} ===")
                print("  (the model is temporarily unavailable - run the script again)")
                return
            await asyncio.sleep(2 * attempt)

    print(f"\n=== {doc_id} ===")
    if result:
            # output_key may store the result as a dict or a JSON string.
            if isinstance(result, str):
                result = json.loads(result)
            print(f"  category:   {result.get('category')}")
            print(f"  confidence: {result.get('confidence')}")
            print(f"  summary:    {result.get('summary')}")
    else:
            # Until the agent sets output_schema and output_key, the result is
            # plain text. Complete Steps 2 and 3 in doc_classifier/agents.py.
            print("  (no structured result - finish Steps 2-3 in doc_classifier/agents.py)")
            print(f"  raw model text: {final_response}")

async def main() -> None:
    runner = InMemoryRunner(agent=root_agent, app_name=APP_NAME)
    for doc_id, text in DOCUMENTS_METADATA.items():
        await document_classifier(runner, doc_id, text)


if __name__ == "__main__":
    asyncio.run(main())