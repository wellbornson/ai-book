# Implementation Plan: RAG Chatbot for Published Book

**Branch**: `002-rag-chatbot` | **Date**: 2025-12-20 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/002-rag-chatbot/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of an AI-powered chatbot that enables users to interact with published book content using Retrieval-Augmented Generation (RAG). The system will support both full-book queries and user-selected text only mode, using Cohere's API exclusively for embeddings and generation. The solution will feature a FastAPI backend with Qdrant Cloud for vector storage and Neon Serverless Postgres for chat history, ensuring responses are accurate, cited, and free of hallucinations.

## Technical Context

**Language/Version**: Python 3.11
**Primary Dependencies**: FastAPI, LangChain, Cohere, Qdrant-client, SQLAlchemy/asyncpg, Pydantic
**Storage**: Qdrant Cloud (vector database), Neon Serverless Postgres (relational DB)
**Testing**: pytest with unit, integration, and contract tests
**Target Platform**: Linux server (deployable to Vercel/Heroku/Render)
**Project Type**: Web application (backend API with potential frontend integration)
**Performance Goals**: API responses <2 seconds for typical queries, handle multiple concurrent users
**Constraints**: No OpenAI dependencies, use free tiers where possible, max dependencies as specified in constitution
**Scale/Scope**: Support multiple books and concurrent users within free tier limitations

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Based on the project constitution, this implementation plan confirms compliance with all core principles:

1. **Accuracy and Faithfulness to Content**: Using RAG approach with proper citations
2. **Dual Mode Operation**: Supporting both full-book and selected text modes
3. **Cohere API Exclusivity**: Using only Cohere's embed-english-v3.0/embed-multilingual-v3.0 and Command R/R+ models
4. **Secure, Scalable, and Maintainable Code**: Following clean, modular architecture with proper error handling
5. **Efficient Large-Scale Processing**: Using appropriate chunk sizes (500-1000 tokens) with overlap (200 tokens)
6. **Comprehensive Testing**: Including unit tests for key components (ingestion, retrieval, API endpoints)

Post-design constitution check confirms continued compliance after detailed architecture decisions.

## Project Structure

### Documentation (this feature)

```text
specs/002-rag-chatbot/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── chat_session.py
│   │   ├── book_content.py
│   │   ├── user_query.py
│   │   ├── retrieved_context.py
│   │   └── generated_response.py
│   ├── services/
│   │   ├── rag_service.py
│   │   ├── embedding_service.py
│   │   ├── retrieval_service.py
│   │   ├── generation_service.py
│   │   ├── ingestion_service.py
│   │   └── session_service.py
│   ├── api/
│   │   ├── main.py
│   │   ├── book_routes.py
│   │   ├── chat_routes.py
│   │   └── query_routes.py
│   └── config/
│       ├── settings.py
│       └── database.py
└── tests/
    ├── unit/
    │   ├── test_rag_service.py
    │   ├── test_embedding_service.py
    │   └── test_retrieval_service.py
    ├── integration/
    │   ├── test_book_ingestion.py
    │   └── test_chat_flow.py
    └── contract/
        └── test_api_contracts.py
```

**Structure Decision**: Web application structure selected with backend API implementation. The backend contains models representing the key entities from the spec, services implementing the core functionality (RAG, embeddings, retrieval, etc.), API routes for user interactions, and configuration files. The test structure includes unit, integration, and contract tests as required by the constitution.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
