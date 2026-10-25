import asyncio

from dotenv import load_dotenv
from google.adk.runners import InMemoryRunner
from google.genai import types

from doc_extraction_agent.agent import data_extractor_agent, data_extraction

load_dotenv()

APP_NAME = "city_assistant_demo"
USER_ID = "student"
SESSION_ID = "async-session"


async def main() -> None:

    runner = InMemoryRunner(agent=data_extractor_agent, app_name=APP_NAME)
    session = await runner.session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
        state={"user:name": "Shiva Dasari"}
    )
    print(f"Session created: {session}")
    message = types.Content(
        role="user",
        parts=[types.Part(text=(
                    "Extract the INTERNATIONAL AIR WAYBILL NO, total invoice price, SHIPPER address,CONSIGNEE address "
                    "from the commercial invoice using the "
                    "data_extraction tool which takes file name as input." 
                    "Return JSON only."
                    "file name is fedex_commercial_invoice_filled_sample.pdf"
                ))],
    )
    async for event in runner.run_async(
        user_id=USER_ID, session_id=SESSION_ID, new_message=message
    ):
        print(f"author={event.author} final={event.is_final_response()}")
        if event.is_final_response() and event.content and event.content.parts:
            print(event.content.parts[0].text)

if __name__ == "__main__":
    asyncio.run(main())