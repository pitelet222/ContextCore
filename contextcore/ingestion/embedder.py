"""Embed chunks using dense (OpenAI/Anthropic-compatible) and optional sparse vectors."""

from __future__ import annotations
import openai
from contextcore.config import get_settings


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Return dense embeddings for a batch of texts."""
    settings = get_settings()
    client = openai.OpenAI(api_key=settings.openai_api_key)
    response = client.embeddings.create(model=settings.embedding_model, input=texts)
    return [item.embedding for item in response.data]
