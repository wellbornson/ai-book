---
id: 1
title: Create RAG Chatbot Constitution
stage: constitution
date_iso: 2025-12-20
surface: agent
model: Qwen
feature: rag-chatbot
branch: main
user: wellbornsonAi
command: /sp.constitution
labels: ["constitution", "rag", "chatbot", "cohere"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - ".specify/memory/constitution.md"
  - "README.md"
tests: []
outcome: "Successfully created project constitution for Integrated RAG Chatbot for Published Book"
evaluation: "Constitution includes all required principles, standards, constraints, and success criteria"
---

# Create RAG Chatbot Constitution

## Prompt Text

```
/sp.constitution **Project: Integrated RAG Chatbot for Published Book**

**Core Principles:**
 Accuracy and faithfulness to book content – always ground responses in retrieved contexts
 Support for both full-book queries and user-selected text only mode
 Use Cohere API exclusively for embeddings and generation (no OpenAI)
 Secure, scalable, and maintainable code with proper error handling
 Clean, modular architecture following best practices

**Key Standards:**
 Embeddings: Cohere embed-english-v3.0 or embed-multilingual-v3.0 (input_type="search_document" for docs, "search_query" for queries)
 Generation: Cohere Command R or R+ model with streaming support
 Vector Database: Qdrant Cloud (free tier), with proper collection configuration (1024-dim vectors, Cosine similarity)
 Backend: FastAPI with async endpoints, Pydantic models, Uvicorn server
 Orchestration: LangChain for RAG chains, retrievers, and document loaders
 Relational DB: Neon Serverless Postgres for chat history, user sessions, and selected text metadata
 Code Style: Python 3.11+, type hints, black formatting, comprehensive docstrings
 Testing: Include unit tests for key components (ingestion, retrieval, API endpoints)

**Constraints:**
 No OpenAI dependencies or API keys
 Use free tiers where possible (Qdrant Cloud Free, Neon, Cohere trial if needed)
 Handle large book content efficiently (chunk size ~500-1000 tokens, overlap 200)
 Support selected text: Endpoint to accept user-highlighted text, embed temporarily or store per session
 Deployment-ready: Include Dockerfile, .env example, README with setup instructions
 Max dependencies: Stick to langchain, cohere, qdrant-client, fastapi, sqlalchemy/asyncpg for Neon

**Success Criteria:**
 Chatbot accurately answers questions from full book content with citations
 Seamlessly handles queries restricted to user-selected text
 API endpoints respond <2s for typical queries
 Full ingestion pipeline works for a sample book (PDF/text)
 Embeddable frontend widget or API for integration into book viewer
 Zero hallucinations outside provided context
 Code is production-quality, deployable to Vercel/Heroku/Render
```

## Response Text

Successfully created the constitution for the Integrated RAG Chatbot for Published Book project with the following elements:

- Core Principles section with 6 specific principles:
  1. Accuracy and Faithfulness to Content
  2. Dual Mode Operation
  3. Cohere API Exclusivity
  4. Secure, Scalable, and Maintainable Code
  5. Efficient Large-Scale Processing
  6. Comprehensive Testing

- Key Standards section with technology stack details
- Constraints section with project limitations
- Success Criteria section with measurable outcomes
- Governance section with amendment and compliance procedures

Also updated the README.md file to reflect the project's purpose and technology stack.