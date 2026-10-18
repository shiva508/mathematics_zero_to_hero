from google.adk.agents.llm_agent import Agent
from google.adk.agents import LlmAgent
import os

POLICIES = {
    "returns": "You have 30 days from delivery to return an item for a full refund.",
    "shipping": "Standard shipping takes 5 business days; expedited takes 2.",
    "warranty": "Every product carries a 1-year limited warranty against defects.",
}

def get_policy(topic: str) -> dict:
    """Looks up the official store policy for a topic.

    Args:
        topic: The policy topic - one of "returns", "shipping", or "warranty".
    """
    key = topic.strip().lower()
    if key not in POLICIES:
        return {
            "status": "error",
            "error_message": f"No policy found for topic '{topic}'.",
        }
    return {"status": "success", "topic": key, "policy": POLICIES[key]}

root_agent = LlmAgent(
    model=os.getenv("ADK_MODEL", "ollama_chat/llama3.2:3b"),
    name='policy_agent',
    description='Answers customer questions about store policies.',
    instruction=(
        "You answer customer questions about store policies. Always call "
        "the get_policy tool to retrieve the official policy text, then "
        "answer based only on what it returns. Keep answers to one sentence."
    ),
    tools=[get_policy]
)

agent = root_agent