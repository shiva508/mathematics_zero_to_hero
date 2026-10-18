"""Core Lab - a customer-support agent with guardrail callbacks.

The agent answers order-status questions. You will add two guardrails:

  Step 1  - block_injection: an input guardrail (before-model callback)
  Step 2  - redact_card_numbers: an output guardrail (after-model callback)

Both are marked "# YOUR CODE HERE". When you finish, run:

    uv run run_agent.py
"""

import os
import re
from google.adk.agents import LlmAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.genai import types


# A tiny mock order database.
ORDERS = {
    "A100": "shipped, arriving Tuesday",
    "A200": "processing, ships within 24 hours",
    "A300": "delivered",
}

def get_order_status(order_id: str) -> dict:
    """Looks up the delivery status of an order.

    Args:
        order_id: The order identifier, such as "A100".
    """
    status = ORDERS.get(order_id.strip().upper())
    if status is None:
        return {
            "status": "error",
            "error_message": f"No order found with id '{order_id}'.",
        }
    return {"status": "success", "order_id": order_id, "delivery_status": status}


def _last_user_text(llm_request: LlmRequest) -> str:
    """Returns the text of the most recent user message in the request."""
    for content in reversed(llm_request.contents or []):
        if content.role == "user" and content.parts:
            return " ".join(p.text for p in content.parts if p.text)
    return ""


def block_injection(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> LlmResponse | None:
    """Input guardrail: blocks obvious prompt-injection attempts."""
    # YOUR CODE HERE - Step 1
    # 1. Get the latest user text with _last_user_text(llm_request).
    # 2. If it contains "ignore previous instructions" (case-insensitive),
    #    return an LlmResponse whose content is a model-role types.Content
    #    with a short refusal - this SKIPS the model call.
    # 3. Otherwise return None so the model runs normally.

    last_user_text = _last_user_text(llm_request)
    if "ignore previous instructions" in last_user_text.lower():
        return LlmResponse(
            content=types.Content(
                role="model",
                parts=[
                    types.Part(
                        text="I can't act on that request. I can only help "
                        "with order-status questions."
                    )
                ],
            )
        )
    return None


def redact_card_numbers(
    callback_context: CallbackContext, llm_response: LlmResponse
) -> LlmResponse | None:
    """Output guardrail: redacts card-like digit sequences from the reply."""
    # YOUR CODE HERE - Step 2
    # 1. If llm_response has no content or parts, return None.
    # 2. Read the reply text from llm_response.content.parts[0].text.
    # 3. Replace card-like digit runs using:
    #       re.sub(r"\b\d(?:[ -]?\d){12,18}\b", "[redacted]", text)
    # 4. If the text changed, print
    #       "[guardrail] redacted card-like digits from reply"
    #    and return a new LlmResponse with the redacted text as a
    #    model-role types.Content. Otherwise return None.
    if not llm_response.content or not llm_response.content.parts:
        return None
    text = llm_response.content.parts[0].text or ""
    redacted_text = re.sub(r"\b\d(?:[ -]?\d){12,18}\b", "[redacted]", text)
    if redacted_text != text:
        print("[guardrail] redacted card-like digits from reply")
        return LlmResponse(
            content=types.Content(
                role="model",
                parts=[types.Part(text=redacted_text)]
            )
        )
    return None



root_agent = LlmAgent(
    name="support_agent",
    model=os.getenv("ADK_MODEL", "ollama_chat/llama3.2:3b"),
    description="Answers customer order-status questions.",
    instruction=(
        "You are a customer-support assistant. Use the get_order_status "
        "tool to answer questions about an order. Be brief and friendly. "
        "Never repeat back full card numbers a customer sends you."
    ),
    tools=[get_order_status],
    before_model_callback=block_injection,
    after_model_callback=redact_card_numbers,
)
