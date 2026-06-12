"""FastAPI application entry-point."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from contextcore.api.routers import query, ingest, health

app = FastAPI(title="ContextCore API", version="0.1.0")
app.include_router(health.router)
app.include_router(query.router, prefix="/api/v1")
app.include_router(ingest.router, prefix="/api/v1")

app.mount("/ui", StaticFiles(directory=Path(__file__).parent / "static", html=True), name="ui")


@app.get("/")
async def root() -> RedirectResponse:
    return RedirectResponse(url="/ui")
