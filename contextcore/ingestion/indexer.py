"""Index embedded chunks into Qdrant."""

from __future__ import annotations
from uuid import uuid4
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams
from contextcore.config import get_settings
from contextcore.ingestion.chunker import Chunk


def get_client() -> QdrantClient:
    s = get_settings()
    return QdrantClient(host=s.qdrant_host, port=s.qdrant_port)


def ensure_collection(client: QdrantClient, dim: int) -> None:
    s = get_settings()
    existing = [c.name for c in client.get_collections().collections]
    if s.qdrant_collection not in existing:
        client.create_collection(
            collection_name=s.qdrant_collection,
            vectors_config=VectorParams(size=dim, distance=Distance.COSINE),
        )


def index_chunks(chunks: list[Chunk], embeddings: list[list[float]]) -> None:
    s = get_settings()
    client = get_client()
    ensure_collection(client, len(embeddings[0]))
    points = [
        PointStruct(id=str(uuid4()), vector=vec, payload={"text": c.text, **c.metadata})
        for c, vec in zip(chunks, embeddings)
    ]
    client.upsert(collection_name=s.qdrant_collection, points=points)
