"""Router agent: classify and decompose an incoming query into sub-queries."""

from __future__ import annotations
import json
import anthropic
import agentops
from contextcore.config import get_settings

DECOMPOSE_PROMPT = """You are a query planning assistant.
Given the user query, output a JSON object with:
  - "sub_queries": list of 1-4 focused sub-questions that together answer the query
  - "source_hint": one of ["internal_docs", "database", "web", "mixed"]

Respond ONLY with valid JSON. No markdown, no explanation."""

_settings = get_settings()
if _settings.agentops_api_key:
    agentops.init(api_key=_settings.agentops_api_key, default_tags=["contextcore"])


def decompose_query(query: str) -> dict:
    s = get_settings()
    client = anthropic.Anthropic(api_key=s.anthropic_api_key)
    msg = client.messages.create(
        model=s.llm_model,
        max_tokens=512,
        system=DECOMPOSE_PROMPT,
        messages=[{"role": "user", "content": query}],
    )
    return json.loads(msg.content[0].text)
