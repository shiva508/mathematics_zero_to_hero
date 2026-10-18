"""Challenge 1 - Share data between tools with the tool context.

Two tools cooperate within a single turn: add_to_cart records items in
temporary state, and get_cart_summary reads them back. Complete the two
tool bodies marked "# YOUR CODE HERE".

Run from the files/ directory:

    uv run challenge1_cart.py
"""

import asyncio
from dotenv import load_dotenv
from google.adk.runners import InMemoryRunner
from google.genai import types
from agent import cart_assistant_agent

load_dotenv()

APP_NAME = "store_cart_assistant"
USER_ID = "student"

async def run_cart_assistant()->None:
    runner = InMemoryRunner(agent=cart_assistant_agent ,app_name=APP_NAME)
    init_session = await runner.session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id="session-1")
    query = types.Content(role="user", parts=[types.Part(text="Add a notebook and a wireless mouse to my cart, "
                "then summarize my cart.")])
    async for event in runner.run_async(user_id=USER_ID, session_id="session-1", new_message=query):
        if event.is_final_response() and event.content and event.content.parts:
            print(event.content.parts[0].text)


if __name__ == "__main__":
    asyncio.run(run_cart_assistant())

