# ContextCore

> Adaptive enterprise RAG — multi-hop reasoning, session memory, agentic routing.

## Quick start

```bash
cp .env.example .env          # fill in your keys (see Configuration below)
docker compose up -d          # start Qdrant, Redis, MLflow
pip install -e ".[dev]"        # install Python package + dev deps
python -m contextcore.ingestion.cli --source ./sample_docs   # index sample documents
uvicorn contextcore.api.main:app --reload --host 0.0.0.0 --port 8000   # run the API
```

Then open **http://localhost:8000** — it redirects to a simple chat UI (`/ui`) for
asking questions about the indexed documents. Interactive API docs are at `/docs`.

If you have GNU Make available, the equivalent `make docker-up`, `make install`,
`make ingest SOURCE=./sample_docs` and `make dev` targets work the same way
(`make dev` adds `--reload`).

### Windows note

`unstructured` depends on `python-magic`, which needs the native `libmagic`
library. On Windows, install the bundled binary instead:

```bash
pip install python-magic-bin
```

## Configuration

Required in `.env`:

- `ANTHROPIC_API_KEY` — used by the router (query decomposition) and synthesiser
- `OPENAI_API_KEY` — used for embeddings (`text-embedding-3-small`)

Optional:

- `AGENTOPS_API_KEY` — enables [AgentOps](https://agentops.ai) session tracing for
  the agent pipeline; if unset, tracing is skipped
- `LANGSMITH_API_KEY`, `MLFLOW_TRACKING_URI` — observability
- `S3_BUCKET` / `S3_REGION` — only needed if ingesting from `s3://` sources

Everything else (Qdrant/Redis hosts, ports, collection names, etc.) has sensible
defaults for the local `docker-compose` stack.

## Architecture

```
Client layer  →  Agent layer (router · planner · memory · synthesiser)
             →  RAG core   (chunker · embedder · retriever · generator)
             →  Data layer (Qdrant · Redis · S3 · MLflow)
```

A query is decomposed into sub-queries (router), each sub-query triggers a
retrieval hop against Qdrant with cross-encoder reranking (rag), hop results
accumulate in a `PlanState` (planner), and the synthesiser produces a grounded
answer with a confidence score and citation indices back to retrieved chunks.
Conversation turns are persisted in Redis (memory) and, if `AGENTOPS_API_KEY`
is set, agent runs are traced via AgentOps.

## Project structure

```
contextcore/
├── config/          Settings (pydantic-settings)
├── ingestion/       Loader · chunker · embedder · indexer · CLI
├── memory/          Redis-backed session store
├── agent/           Router · planner · synthesiser
├── rag/             Retriever (ANN + rerank) · pipeline orchestrator
└── api/             FastAPI app + routers (query · ingest · health) + static/ (chat UI)
tests/
├── unit/            Chunker, planner logic
└── integration/     API smoke tests
sample_docs/         Example documents for testing ingestion and multi-hop retrieval
notebooks/           Exploration and evaluation
docs/                Architecture · API reference · Deployment
```

## Running tests

```bash
make test
# or: pytest tests/ -v --cov=contextcore --cov-report=term-missing
```
