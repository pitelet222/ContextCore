"""Answer synthesiser: merge multi-hop context, score confidence, attach citations."""

from __future__ import annotations
import anthropic
from contextcore.config import get_settings
from contextcore.agent.planner import PlanState

SYNTH_PROMPT = """You are a precise enterprise knowledge assistant.
Given the user query and the retrieved context passages, produce:
1. A clear, grounded answer referencing only the provided context.
2. A confidence score from 0.0 to 1.0 (how well the context supports the answer).
3. A list of citation indices (0-based) from the context passages used.

Respond in JSON:
{"answer": "...", "confidence": 0.0, "citations": [0, 1]}
No markdown, no explanation outside the JSON."""


def synthesise(state: PlanState) -> dict:
    s = get_settings()
    client = anthropic.Anthropic(api_key=s.anthropic_api_key)
    context_text = "\n\n".join(
        f"[{i}] {t}" for i, t in enumerate(state.context_buffer)
    )
    user_msg = f"Query: {state.original_query}\n\nContext:\n{context_text}"
    msg = client.messages.create(
        model=s.llm_model,
        max_tokens=1024,
        system=SYNTH_PROMPT,
        messages=[{"role": "user", "content": user_msg}],
    )
    import json
    return json.loads(msg.content[0].text)
