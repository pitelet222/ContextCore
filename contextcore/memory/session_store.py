"""Short-term session memory backed by Redis with vector-similarity recall."""

from __future__ import annotations
import json
import redis
from contextcore.config import get_settings


class SessionStore:
    def __init__(self, session_id: str) -> None:
        s = get_settings()
        self._r = redis.Redis(host=s.redis_host, port=s.redis_port, decode_responses=True)
        self._key = f"session:{session_id}:history"
        self._ttl = s.redis_ttl_seconds

    def append(self, role: str, content: str) -> None:
        entry = json.dumps({"role": role, "content": content})
        self._r.rpush(self._key, entry)
        self._r.expire(self._key, self._ttl)

    def get_history(self, last_n: int = 10) -> list[dict]:
        raw = self._r.lrange(self._key, -last_n, -1)
        return [json.loads(r) for r in raw]

    def clear(self) -> None:
        self._r.delete(self._key)
