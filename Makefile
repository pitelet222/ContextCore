.PHONY: install dev test lint format docker-up docker-down ingest

install:
	pip install -e ".[dev]"

dev:
	uvicorn contextcore.api.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest tests/ -v --cov=contextcore --cov-report=term-missing

lint:
	ruff check . && mypy contextcore/

format:
	ruff format .

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

ingest:
	python -m contextcore.ingestion.cli --source $(SOURCE) --collection $(COLLECTION)
