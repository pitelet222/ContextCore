"""Multi-hop query planner: orchestrates sequential retrieval rounds."""

from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class HopResult:
    sub_query: str
    retrieved_chunks: list[dict]
    hop_index: int


@dataclass
class PlanState:
    original_query: str
    sub_queries: list[str]
    completed_hops: list[HopResult] = field(default_factory=list)
    context_buffer: list[str] = field(default_factory=list)

    @property
    def is_complete(self) -> bool:
        return len(self.completed_hops) >= len(self.sub_queries)

    def next_sub_query(self) -> str | None:
        idx = len(self.completed_hops)
        return self.sub_queries[idx] if idx < len(self.sub_queries) else None

    def record_hop(self, sub_query: str, chunks: list[dict]) -> None:
        hop = HopResult(sub_query, chunks, len(self.completed_hops))
        self.completed_hops.append(hop)
        for c in chunks:
            self.context_buffer.append(c.get("text", ""))
