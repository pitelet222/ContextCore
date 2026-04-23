"""CLI entry-point: python -m contextcore.ingestion.cli --source ./docs"""

import argparse
from pathlib import Path
from contextcore.ingestion.loader import load_documents
from contextcore.ingestion.chunker import semantic_chunk
from contextcore.ingestion.embedder import embed_texts
from contextcore.ingestion.indexer import index_chunks
from loguru import logger


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest documents into ContextCore")
    parser.add_argument("--source", required=True, help="Path or S3 URI to ingest")
    parser.add_argument("--collection", default=None, help="Override Qdrant collection name")
    args = parser.parse_args()

    logger.info(f"Ingesting from: {args.source}")
    for doc in load_documents(args.source):
        chunks = semantic_chunk(doc)
        if not chunks:
            continue
        texts = [c.text for c in chunks]
        embeddings = embed_texts(texts)
        index_chunks(chunks, embeddings)
        logger.info(f"Indexed {len(chunks)} chunks")
    logger.success("Ingestion complete.")


if __name__ == "__main__":
    main()
