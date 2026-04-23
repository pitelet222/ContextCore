"""End-to-end RAG pipeline: decompose → hop → synthesise."""

from __future__ import annotations
from contextcore.agent.router import decompose_query
from contextcore.agent.planner import PlanState
from contextcore.agent.synthesiser import synthesise
from contextcore.rag.retriever import retrieve
from contextcore.memory.session_store import SessionStore
from loguru import logger


def run_pipeline(query: str, session_id: str) -> dict:
    """Run the full multi-hop RAG pipeline and return a structured result."""
    memory = SessionStore(session_id)
    memory.append("user", query)

    # 1. Decompose
    plan_data = decompose_query(query)
    sub_queries: list[str] = plan_data.get("sub_queries", [query])
    logger.info(f"Sub-queries: {sub_queries}")

    state = PlanState(original_query=query, sub_queries=sub_queries)

    # 2. Multi-hop retrieval loop
    while not state.is_complete:
        sq = state.next_sub_query()
        if sq is None:
            break
        chunks = retrieve(sq)
        state.record_hop(sq, chunks)
        logger.info(f"Hop {len(state.completed_hops)}: retrieved {len(chunks)} chunks")

    # 3. Synthesise
    result = synthesise(state)
    memory.append("assistant", result.get("answer", ""))
    return result
