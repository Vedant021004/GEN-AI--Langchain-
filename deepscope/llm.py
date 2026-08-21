"""Groq chat model wiring plus small helpers for structured replies."""

import json
import re

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq

from deepscope.config import Settings

_JSON_ARRAY = re.compile(r"\[.*?\]", re.DOTALL)


def build_llm(settings: Settings) -> BaseChatModel:
    """Create the chat model used by every node of the graph."""
    if not settings.has_llm:
        raise RuntimeError("GROQ_API_KEY is not set; DeepScope needs it to reason.")
    return ChatGroq(
        model=settings.model,
        temperature=settings.temperature,
        api_key=settings.groq_api_key,
    )


def ask(llm: BaseChatModel, system: str, user: str) -> str:
    """Single-turn completion returning plain text."""
    reply = llm.invoke([SystemMessage(content=system), HumanMessage(content=user)])
    content = reply.content
    if isinstance(content, str):
        return content.strip()
    parts = [block for block in content if isinstance(block, str)]
    return "\n".join(parts).strip()


def parse_string_list(text: str) -> list[str]:
    """Best-effort extraction of a JSON string array from an LLM reply.

    Falls back to bullet/newline parsing so a chatty model never breaks the run.
    """
    match = _JSON_ARRAY.search(text)
    if match:
        try:
            parsed = json.loads(match.group(0))
        except json.JSONDecodeError:
            parsed = None
        if isinstance(parsed, list):
            items = [str(item).strip() for item in parsed if str(item).strip()]
            if items:
                return items

    items = []
    for line in text.splitlines():
        cleaned = line.strip().lstrip("-*0123456789.) ").strip()
        if cleaned and not cleaned.lower().startswith("here"):
            items.append(cleaned)
    return items
