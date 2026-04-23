from contextcore.ingestion.chunker import semantic_chunk


def test_basic_chunking():
    doc = {"text": " ".join([f"word{i}" for i in range(600)]), "metadata": {}}
    chunks = semantic_chunk(doc, max_tokens=100, overlap_tokens=20)
    assert len(chunks) > 1
    assert all(c.text for c in chunks)


def test_single_chunk():
    doc = {"text": "short text", "metadata": {}}
    chunks = semantic_chunk(doc, max_tokens=100)
    assert len(chunks) == 1
    assert chunks[0].chunk_index == 0
