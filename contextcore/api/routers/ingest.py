"""Ingest endpoint — accepts a file path or S3 URI and indexes it."""

from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel
from contextcore.ingestion.loader import load_documents
from contextcore.ingestion.chunker import semantic_chunk
from contextcore.ingestion.embedder import embed_texts
from contextcore.ingestion.indexer import index_chunks
from loguru import logger

router = APIRouter(tags=["ingest"])


class IngestRequest(BaseModel):
    source: str


def _ingest_task(source: str) -> None:
    for doc in load_documents(source):
        chunks = semantic_chunk(doc)
        if not chunks:
            continue
        embeddings = embed_texts([c.text for c in chunks])
        index_chunks(chunks, embeddings)
    logger.success(f"Ingestion complete: {source}")


@router.post("/ingest")
async def ingest_endpoint(req: IngestRequest, background_tasks: BackgroundTasks) -> dict:
    background_tasks.add_task(_ingest_task, req.source)
    return {"status": "ingestion_started", "source": req.source}
