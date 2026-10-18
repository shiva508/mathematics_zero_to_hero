"""Challenge 2 - Route documents to specialized extraction agents.

The classifier tells you *what* a document is. This challenge adds two
specialized agents that extract *details* specific to each type, and a
router that sends each document to the right specialist.

The two detail schemas and the two specialist agents are provided.
Complete route_and_extract().

Run from the files/ directory:

    uv run specilist_router.py
"""

import asyncio
import json
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.runners import InMemoryRunner
from google.genai import types

from document_store import DOCUMENTS_METADATA
from agent import review_agent, invoice_agent, root_agent

load_dotenv()

APP_NAME = "doc_specialist_router"
USER_ID = "student"

# Maps a category from the classifier to its specialist agent.
SPECIALISTS = {"invoice": invoice_agent, "product_review": review_agent}



async def common_classifier(agent: LlmAgent, text: str, state_key:str) -> dict:
    """Run the classifier once and return the result as a dict."""
    session_id = f"s-{agent.name}-{abs(hash(text)) % 100000}"
    runner = InMemoryRunner(agent=agent, app_name=APP_NAME)
    initial_session = await runner.session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=session_id)
    #print(f"Session created: {initial_session}")
    message = types.Content(role="user", parts=[types.Part(text=text)])
    async for _event in runner.run_async(user_id=USER_ID, session_id=session_id, new_message=message):
        pass
    end_session = await runner.session_service.get_session(app_name=APP_NAME, user_id=USER_ID, session_id=session_id)
    #print(f"Session retrieved: {end_session}")
    result = end_session.state.get(state_key)
    if isinstance(result, str):
        result = json.loads(result)
    return result or {}

async def route_and_extract(text: str) -> dict:
    """Classify a document, then extract details with a specialist.

    YOUR CODE HERE - Challenge 2
    1. Run classifier_agent on the text with run_agent(...). The
       classifier stores its result under the state key "classification".
       Read the "category" from that result.
    2. Look up the matching specialist in SPECIALISTS. If there is no
       specialist for the category, return {"category": category,
       "details": None}.
    3. Run the specialist agent on the text; specialists store their
       result under the state key "details". Return a dict with both the
       "category" and the extracted "details".
    """
    classification = await common_classifier(root_agent, text, "classification")
    #print(f"Classification result: {classification}")
    category = classification.get("category", "unknown")
    specialist = SPECIALISTS.get(category)
    print(f"Specialist for category '{category}': {specialist.name if specialist else None}")
    if specialist is None:
        return {"category": category, "details": None}
    details = await common_classifier(specialist, text, "details")
    return {"category": category, "details": details}



async def main() -> None:
    for doc_id, text in DOCUMENTS_METADATA.items():
        result = await route_and_extract(text)
        print(f"{doc_id}: {result}")


if __name__ == "__main__":
    asyncio.run(main())