"""Load raw documents from local paths, S3 or URLs using Unstructured."""

from pathlib import Path
from typing import Iterable
from unstructured.partition.auto import partition


def load_documents(source: str | Path) -> Iterable[dict]:
    """Yield raw text elements from any supported source."""
    path = Path(source)
    if path.is_dir():
        for file_path in sorted(path.rglob("*")):
            if file_path.is_file():
                yield from _partition_file(file_path)
    else:
        yield from _partition_file(source)


def _partition_file(source: str | Path) -> Iterable[dict]:
    elements = partition(filename=str(source))
    for el in elements:
        yield {"text": el.text, "metadata": el.metadata.to_dict()}
