"""ANN retrieval from Qdrant + cross-encoder reranking."""

from __future__ import annotations
from qdrant_client import QdrantClient
from contextcore.config import get_settings
from contextcore.ingestion.embedder import embed_texts
from contextcore.ingestion.indexer import get_client
from sentence_transformers import CrossEncoder

# Loaded once at import time to avoid reloading the model on every query
_reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def retrieve(query: str, top_k: int = 10, rerank_top: int = 5) -> list[dict]:
    s = get_settings()
    client: QdrantClient = get_client()
    query_vec = embed_texts([query])[0]
    results = client.query_points(
        collection_name=s.qdrant_collection,
        query=query_vec,
        limit=top_k,
        with_payload=True,
    ).points
    pairs = [(query, r.payload.get("text", "")) for r in results]
    scores = _reranker.predict(pairs)
    ranked = sorted(zip(results, scores), key=lambda x: x[1], reverse=True)[:rerank_top]
    ranked = [r for r, _ in ranked]
    return [{"text": r.payload.get("text", ""), "score": r.score, "id": str(r.id)} for r in ranked]
