"""Load raw documents from local paths, S3 or URLs using Unstructured."""

from pathlib import Path
from typing import Iterable
from unstructured.partition.auto import partition


def load_documents(source: str | Path) -> Iterable[dict]:
    """Yield raw text elements from any supported source."""
    elements = partition(filename=str(source))
    for el in elements:
        yield {"text": el.text, "metadata": el.metadata.to_dict()}
