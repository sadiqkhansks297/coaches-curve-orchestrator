"""
Orchestrator — routes messages to the right workflow.

Prototype intents: question, lead_prep
Production intents (later): framework_extract, milestone_check, draft_message
"""

import re

from src.knowledge import get_knowledge_store
from src.llm import get_llm_provider
from src.orchestrator.prompts import LEAD_PREP_PROMPT, SYSTEM_PROMPT


def classify_intent(message: str) -> str:
    """Simple keyword-based intent classification. Upgrade to LLM classifier in production."""
    lower = message.lower()
    lead_signals = ["prep", "prepare", "call with", "meeting with", "strategy session", "brief"]
    if any(signal in lower for signal in lead_signals):
        return "lead_prep"
    return "question"


def handle_message(message: str) -> str:
    """Main entry point — classify, retrieve context, generate response."""
    knowledge = get_knowledge_store()
    llm = get_llm_provider()
    intent = classify_intent(message)

    if intent == "lead_prep":
        context = knowledge.search("strategy session prep ideal client qualification")
        user_prompt = (
            f"{LEAD_PREP_PROMPT}\n\n"
            f"## Business Context\n{context}\n\n"
            f"## Prospect Notes (from CEO)\n{message}"
        )
        return llm.generate(SYSTEM_PROMPT, user_prompt)

    # Default: question
    context = knowledge.search(message)
    user_prompt = f"## Business Context\n{context}\n\n## Question\n{message}"
    return llm.generate(SYSTEM_PROMPT, user_prompt)
