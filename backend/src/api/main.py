import sys
import os

# Add project root to sys.path to resolve 'backend' imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

from fastapi import FastAPI
from backend.src.config.settings import settings
from backend.src.api import book_routes, chat_routes, query_routes
from backend.src.utils.error_handler import setup_error_handlers
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Startup
    print("Starting up RAG Chatbot for Published Book...")

    # Any startup tasks can go here

    yield

    # Shutdown
    print("Shutting down RAG Chatbot for Published Book...")


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application
    """
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        lifespan=lifespan
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:5000", "*"],  # Allow more origins including wildcard for development
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        allow_origin_regex=r"https?://localhost(:[0-9]+)?",  # Allow any localhost port
    )

    # Setup error handlers
    setup_error_handlers(app)

    # Include API routes
    app.include_router(book_routes.router, prefix="/api/v1", tags=["books"])
    app.include_router(chat_routes.router, prefix="/api/v1", tags=["chat"])
    app.include_router(query_routes.router, prefix="/api/v1", tags=["query"])

    @app.get("/")
    async def root():
        return {"message": "Welcome to the RAG Chatbot for Published Book API"}

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )