# Feature Specification: RAG Chatbot for Published Book

**Feature Branch**: `002-rag-chatbot`
**Created**: 2025-12-20
**Status**: Draft
**Input**: User description: "Project: Integrated RAG Chatbot for Published Book **Core Principles:** * Accuracy and faithfulness to book content – always ground responses in retrieved contexts * Support for both full-book queries and user-selected text only mode * Use Cohere API exclusively for embeddings and generation (no OpenAI) * Secure, scalable, and maintainable code with proper error handling * Clean, modular architecture following best practices **Key Standards:** * Embeddings: Cohere embed-english-v3.0 or embed-multilingual-v3.0 (input_type="search_document" for docs, "search_query" for queries) * Generation: Cohere Command R or R+ model with streaming support * Vector Database: Qdrant Cloud (free tier), with proper collection configuration (1024-dim vectors, Cosine similarity) * Backend: FastAPI with async endpoints, Pydantic models, Uvicorn server * Orchestration: LangChain for RAG chains, retrievers, and document loaders * Relational DB: Neon Serverless Postgres for chat history, user sessions, and selected text metadata * Code Style: Python 3.11+, type hints, black formatting, comprehensive docstrings * Testing: Include unit tests for key components (ingestion, retrieval, API endpoints) **Constraints:** * No OpenAI dependencies or API keys * Use free tiers where possible (Qdrant Cloud Free, Neon, Cohere trial if needed) * Handle large book content efficiently (chunk size ~500-1000 tokens, overlap 200) * Support selected text: Endpoint to accept user-highlighted text, embed temporarily or store per session * Deployment-ready: Include Dockerfile, .env example, README with setup instructions * Max dependencies: Stick to langchain, cohere, qdrant-client, fastapi, sqlalchemy/asyncpg for Neon"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Full Book Query (Priority: P1)

As a reader, I want to ask questions about the entire book content so that I can get accurate, cited answers based on the book's information.

**Why this priority**: This is the core functionality of the RAG chatbot - enabling users to interact with the full book content through natural language queries.

**Independent Test**: The system can accept a user query about the book content and return an accurate response with proper citations to the relevant book sections within 2 seconds.

**Acceptance Scenarios**:

1. **Given** a book has been properly ingested into the system, **When** a user submits a question about the book content, **Then** the system returns an accurate response with citations to specific book sections
2. **Given** a user has submitted a query, **When** the system processes the query against the book content, **Then** the response is delivered within 2 seconds
3. **Given** the system retrieves relevant book content, **When** generating a response, **Then** the response contains no information outside the provided book context

---

### User Story 2 - User-Selected Text Query (Priority: P2)

As a reader, I want to select specific text from the book and ask questions only about that selected text so that I can get focused answers on particular passages.

**Why this priority**: This provides users with granular control over the context, allowing for more focused discussions on specific passages.

**Independent Test**: The system can accept user-selected text and respond to queries specifically about that text, ignoring the broader book context.

**Acceptance Scenarios**:

1. **Given** a user has selected specific text from the book, **When** the user asks a question about that text, **Then** the system responds based only on the selected text and not the broader book content
2. **Given** a user has selected text and submitted a query, **When** the system processes the query, **Then** the response is delivered within 2 seconds
3. **Given** a user has selected text, **When** the user asks a question outside the scope of that text, **Then** the system indicates that the answer is not available in the selected text

---

### User Story 3 - Chat History and Session Management (Priority: P3)

As a reader, I want to maintain my conversation history with the chatbot so that I can have coherent, contextual discussions across multiple queries.

**Why this priority**: This enhances the user experience by allowing for conversational continuity and context awareness across multiple interactions.

**Independent Test**: The system can maintain and reference conversation history during a user session, allowing for follow-up questions that reference previous exchanges.

**Acceptance Scenarios**:

1. **Given** a user is in an active session, **When** the user asks a follow-up question that references previous conversation, **Then** the system appropriately uses context from the conversation history
2. **Given** a user session exists, **When** the session ends, **Then** the chat history is properly stored and can be retrieved if needed
3. **Given** a user returns to the application, **When** resuming a previous session, **Then** the system can provide access to relevant conversation history

---

### Edge Cases

- What happens when a user uploads a very large book (hundreds of MB) that exceeds memory limitations?
- How does the system handle queries in a language different from the book's original language?
- What happens when the Cohere API is temporarily unavailable or rate-limited?
- How does the system handle queries that contain sensitive or inappropriate content?
- What happens when the vector database is temporarily unavailable?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST ground all responses in retrieved book contexts with proper citations
- **FR-002**: System MUST support both full-book query mode and user-selected text only mode
- **FR-003**: System MUST use Cohere API exclusively for embeddings and text generation (no OpenAI dependencies)
- **FR-004**: System MUST handle large book content efficiently using appropriate chunking (500-1000 tokens) with overlap (200 tokens)
- **FR-005**: System MUST provide API endpoints that respond within 2 seconds for typical queries
- **FR-006**: System MUST implement proper error handling and security measures
- **FR-007**: Users MUST be able to select specific text from the book and restrict queries to that text
- **FR-008**: System MUST store chat history and user session data in Neon Serverless Postgres
- **FR-009**: System MUST support ingestion of book content from PDF and text formats
- **FR-010**: System MUST ensure zero hallucinations outside the provided book context
- **FR-011**: System MUST provide deployment-ready configuration with Dockerfile and .env example

### Key Entities

- **ChatSession**: Represents a user's conversation with the chatbot, containing metadata and history
- **BookContent**: Represents the book data that has been processed and stored in the vector database
- **UserQuery**: Represents a user's question along with context information (full-book vs selected text mode)
- **RetrievedContext**: Represents the relevant book passages retrieved to answer a specific query
- **GeneratedResponse**: Represents the AI-generated answer with citations to book sections

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users receive accurate, cited responses to book-related questions 95% of the time
- **SC-002**: API endpoints respond to typical queries in under 2 seconds
- **SC-003**: The system successfully ingests and processes a sample book (PDF/text) without errors
- **SC-004**: The system achieves zero hallucinations (responses with information not present in the book) in testing
- **SC-005**: Users can seamlessly switch between full-book and selected-text query modes
- **SC-006**: The application can be successfully deployed using the provided Dockerfile and configuration
- **SC-007**: 90% of users successfully complete their primary information-seeking task on first attempt
