from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # LLM
    anthropic_api_key: str = ""
    openai_api_key: str = ""
    llm_provider: str = "anthropic"
    llm_model: str = "claude-sonnet-4-20250514"

    # Embeddings
    embedding_model: str = "text-embedding-3-small"
    embedding_dim: int = 1536

    # Vector DB
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_collection: str = "contextcore_docs"

    # Redis
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_ttl_seconds: int = 3600

    # Storage
    s3_bucket: str = ""
    s3_region: str = "eu-west-1"

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_secret_key: str = "change_me"

    # Observability
    langsmith_api_key: str = ""
    langsmith_project: str = "contextcore"
    mlflow_tracking_uri: str = "http://localhost:5000"


@lru_cache
def get_settings() -> Settings:
    return Settings()
