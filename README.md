# ContextCore

> Adaptive enterprise RAG — multi-hop reasoning, session memory, agentic routing.

## Quick start

```bash
cp .env.example .env          # fill in your keys
make docker-up                # start Qdrant, Redis, MLflow
make install                  # install Python package + dev deps
make ingest SOURCE=./docs     # index your documents
make dev                      # run the API at http://localhost:8000
```

## Architecture

```
Client layer  →  Agent layer (router · planner · memory · synthesiser)
             →  RAG core   (chunker · embedder · retriever · generator)
             →  Data layer (Qdrant · Redis · S3 · MLflow)
```

## Project structure

```
contextcore/
├── config/          Settings (pydantic-settings)
├── ingestion/       Loader · chunker · embedder · indexer · CLI
├── memory/          Redis-backed session store
├── agent/           Router · planner · synthesiser
├── rag/             Retriever (ANN + rerank) · pipeline orchestrator
└── api/             FastAPI app + routers (query · ingest · health)
tests/
├── unit/            Chunker, planner logic
└── integration/     API smoke tests
notebooks/           Exploration and evaluation
docs/                Architecture · API reference · Deployment
```

## Running tests

```bash
make test
```
