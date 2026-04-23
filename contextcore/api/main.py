"""FastAPI application entry-point."""

from fastapi import FastAPI
from contextcore.api.routers import query, ingest, health

app = FastAPI(title="ContextCore API", version="0.1.0")
app.include_router(health.router)
app.include_router(query.router, prefix="/api/v1")
app.include_router(ingest.router, prefix="/api/v1")
