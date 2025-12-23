import os
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


# Detect if running on Vercel
IS_VERCEL = os.environ.get("VERCEL") == "1"


class Settings(BaseSettings):
    # Database settings
    # On Vercel, the filesystem is read-only, so we use /tmp for the default SQLite DB
    # However, for production, users should set APP_DATABASE_URL to a real DB like Neon
    _default_db = "sqlite+aiosqlite:////tmp/book_chatbot.db" if IS_VERCEL else "sqlite+aiosqlite:///./book_chatbot.db"
    database_url: str = Field(alias="APP_DATABASE_URL", default=_default_db)

    # Cohere settings
    cohere_api_key: str = Field(default="your_cohere_api_key_here")

    # Qdrant settings
    qdrant_url: str = Field(default="your_qdrant_url_here")
    qdrant_api_key: Optional[str] = None

    # Application settings
    app_name: str = "RAG Chatbot for Published Book"
    app_version: str = "0.1.0"
    debug: bool = False
    environment: str = "production" if IS_VERCEL else "development"  # development, staging, production

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