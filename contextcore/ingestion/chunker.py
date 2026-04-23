"""Semantic chunking with configurable overlap and size limits."""

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Chunk:
    text: str
    metadata: dict
    chunk_index: int


def semantic_chunk(
    document: dict,
    max_tokens: int = 512,
    overlap_tokens: int = 64,
) -> list[Chunk]:
    """
    Split a document dict into overlapping chunks.
    Replace with a sentence-boundary splitter for production.
    """
    text: str = document["text"]
    words = text.split()
    chunks: list[Chunk] = []
    step = max_tokens - overlap_tokens
    for i, start in enumerate(range(0, len(words), step)):
        chunk_words = words[start : start + max_tokens]
        if not chunk_words:
            break
        chunks.append(
            Chunk(
                text=" ".join(chunk_words),
                metadata={**document.get("metadata", {}), "chunk_start": start},
                chunk_index=i,
            )
        )
    return chunks
