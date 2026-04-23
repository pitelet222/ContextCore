"""Query endpoint — triggers the full RAG pipeline."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from contextcore.rag.pipeline import run_pipeline

router = APIRouter(tags=["query"])


class QueryRequest(BaseModel):
    query: str
    session_id: str = "default"


class QueryResponse(BaseModel):
    answer: str
    confidence: float
    citations: list[int]


@router.post("/query", response_model=QueryResponse)
async def query_endpoint(req: QueryRequest) -> QueryResponse:
    try:
        result = run_pipeline(req.query, req.session_id)
        return QueryResponse(**result)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
