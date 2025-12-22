<!--
Sync Impact Report:
- Version change: 0.1.0 → 1.0.0
- Modified principles: All principles replaced with RAG Chatbot-specific principles
- Added sections: Key Standards, Constraints, Success Criteria
- Removed sections: None
- Templates requiring updates: ✅ Updated
- Follow-up TODOs: None
-->
# Integrated RAG Chatbot for Published Book Constitution

## Core Principles

### I. Accuracy and Faithfulness to Content
All responses must be grounded in retrieved contexts from the book; No hallucinations outside provided context; Citations required when referencing specific book content.

### II. Dual Mode Operation
Support both full-book queries and user-selected text only mode; Maintain clear separation between global and user-defined context sources.

### III. Cohere API Exclusivity
Use Cohere API exclusively for embeddings and generation (no OpenAI dependencies); Leverage embed-english-v3.0 or embed-multilingual-v3.0 for embeddings with proper input_type specification.

### IV. Secure, Scalable, and Maintainable Code
Implement proper error handling and security measures; Follow clean, modular architecture following best practices; Ensure code is production-quality and deployable.

### V. Efficient Large-Scale Processing
Handle large book content efficiently with appropriate chunk sizes (~500-1000 tokens) and overlap (200 tokens); Optimize for performance with response times under 2 seconds for typical queries.

### VI. Comprehensive Testing
Include unit tests for key components (ingestion, retrieval, API endpoints); Test both full-book and selected text modes; Ensure zero hallucinations outside provided context.

## Key Standards

Technology Stack:
- Embeddings: Cohere embed-english-v3.0 or embed-multilingual-v3.0 (input_type="search_document" for docs, "search_query" for queries)
- Generation: Cohere Command R or R+ model with streaming support
- Vector Database: Qdrant Cloud (free tier), with proper collection configuration (1024-dim vectors, Cosine similarity)
- Backend: FastAPI with async endpoints, Pydantic models, Uvicorn server
- Orchestration: LangChain for RAG chains, retrievers, and document loaders
- Relational DB: Neon Serverless Postgres for chat history, user sessions, and selected text metadata
- Code Style: Python 3.11+, type hints, black formatting, comprehensive docstrings

## Constraints

- No OpenAI dependencies or API keys
- Use free tiers where possible (Qdrant Cloud Free, Neon, Cohere trial if needed)
- Max dependencies: Stick to langchain, cohere, qdrant-client, fastapi, sqlalchemy/asyncpg for Neon
- Support selected text: Endpoint to accept user-highlighted text, embed temporarily or store per session
- Deployment-ready: Include Dockerfile, .env example, README with setup instructions

## Success Criteria

- Chatbot accurately answers questions from full book content with citations
- Seamlessly handles queries restricted to user-selected text
- API endpoints respond <2s for typical queries
- Full ingestion pipeline works for a sample book (PDF/text)
- Embeddable frontend widget or API for integration into book viewer
- Zero hallucinations outside provided context
- Code is production-quality, deployable to Vercel/Heroku/Render

## Governance

This constitution supersedes all other development practices for the Integrated RAG Chatbot for Published Book project. All amendments require documentation with clear justification, approval from project stakeholders, and a migration plan if applicable. All pull requests and code reviews must verify compliance with these principles. All team members must familiarize themselves with these principles before contributing to the project.

**Version**: 1.0.0 | **Ratified**: 2025-01-01 | **Last Amended**: 2025-12-20
