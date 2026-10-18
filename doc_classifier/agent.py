"""Core Lab - Document Classifier agent.

Classifies a document into a category with a confidence score and a
one-sentence summary, returning a validated structured result.

Complete the sections marked "# YOUR CODE HERE", then run:

    uv run classify_documents.py
"""

import os

from google.adk.agents import LlmAgent
from google.adk.models.google_llm import Gemini
from google.genai import types
from pydantic import BaseModel, Field, field_validator
from specilist_models import InvoiceDetails, ReviewDetails

MODEL = Gemini(
    model=os.getenv("ADK_MODEL", "ollama_chat/llama3.2:3b"),
    retry_options=types.HttpRetryOptions(
        attempts=6,
        initial_delay=2.0,
        max_delay=60.0,
        exp_base=2.0,
        jitter=1.0,
        http_status_codes=[408, 429, 500, 502, 503, 504],
    ),
)

# The categories this classifier may assign.
CATEGORIES = ["invoice", "support_ticket", "product_review", "meeting_notes"]


class Classification(BaseModel):
    """The structured result of classifying one document."""

    category: str
    confidence: float = Field(ge=0.0, le=1.0)
    summary: str

    @field_validator("category")
    @classmethod
    def category_validator(cls, value: str) -> str:
        normalized = value.strip().lower()
        if normalized not in CATEGORIES:
            raise ValueError(
                f"category must be one of {CATEGORIES}, got '{value}'"
            )
        return normalized


root_agent = LlmAgent(
    name="doc_classifier",
    model=os.getenv("ADK_MODEL", "ollama_chat/llama3.2:3b"),
    description="Classifies a document into a category.",
    instruction=(
        "Classify the user's document into exactly one of these categories: "
        "invoice, support_ticket, product_review, or meeting_notes. Use the "
        "category exactly as written. Set confidence to a decimal number from "
        "0.0 to 1.0, where 0.0 means not confident and 1.0 means completely "
        "confident. Do not use a rating, score, amount, or other number from "
        "the document as the confidence value. Write a one-sentence summary."
    ),
    output_schema=Classification,
    output_key="classification",
)


review_agent = LlmAgent(
    name="review_extractor",
    model=os.getenv("ADK_MODEL", "ollama_chat/llama3.2:3b"),
    instruction=(
        "Extract a 1-5 star rating, the overall sentiment, and the single "
        "most important point from the product review the user provides."
    ),
    output_schema=ReviewDetails,
    output_key="details",
)

invoice_agent = LlmAgent(
    name="invoice_extractor",
    model=os.getenv("ADK_MODEL", "ollama_chat/llama3.2:3b"),
    instruction=(
        "Extract the vendor, total amount, and due date from the invoice "
        "the user provides."
    ),
    output_schema=InvoiceDetails,
    output_key="details",
)