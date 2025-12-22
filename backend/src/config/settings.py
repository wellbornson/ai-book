from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database settings
    database_url: str = "postgresql+asyncpg://user:password@localhost/dbname"

    # Cohere settings
    cohere_api_key: str

    # Qdrant settings
    qdrant_url: str
    qdrant_api_key: Optional[str] = None

    # Application settings
    app_name: str = "RAG Chatbot for Published Book"
    app_version: str = "0.1.0"
    debug: bool = False
    environment: str = "development"  # development, staging, production

    # RAG settings
    max_tokens: int = 1000
    chunk_overlap: int = 200

    # Auth settings
    expected_bearer_token: str = "test-token"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore"  # Ignore extra environment variables
    }


settings = Settings()