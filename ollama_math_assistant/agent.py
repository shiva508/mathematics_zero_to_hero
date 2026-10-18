from google.adk.agents.llm_agent import Agent



import os

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

# Tell LiteLLM where Ollama is running.
os.environ["OLLAMA_API_BASE"] = "http://localhost:11434"

# Create the agent using a locally running model.
root_agent = Agent(
    name="ollama_assistant",
    model=LiteLlm(
        model="ollama_chat/gemma2:9b"
    ),
    description="A helpful AI assistant powered by Ollama.",
    instruction="""
        You are a helpful AI assistant.

        Answer questions clearly and accurately.
        Explain technical concepts with examples when appropriate.
    """,
)
