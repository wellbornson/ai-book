# Data Model: RAG Chatbot for Published Book

## Entity: ChatSession
**Description**: Represents a user's conversation with the chatbot, containing metadata and history
**Fields**:
- id: UUID (Primary Key)
- user_id: UUID (Foreign Key to user, optional for anonymous sessions)
- created_at: DateTime (Timestamp when session started)
- updated_at: DateTime (Timestamp when last activity occurred)
- title: String (Generated title based on first query)
- metadata: JSON (Additional session data, e.g., book_id, mode: full-book/selected-text)

**Validation Rules**:
- created_at must be before updated_at
- title must be between 5-100 characters
- metadata must include required context information

## Entity: BookContent
**Description**: Represents the book data that has been processed and stored in the vector database
**Fields**:
- id: UUID (Primary Key)
- title: String (Book title)
- author: String (Book author)
- content_hash: String (Hash of original content for deduplication)
- chunk_count: Integer (Number of content chunks)
- created_at: DateTime
- metadata: JSON (Additional book information)

**Validation Rules**:
- title and author are required
- content_hash must be unique
- chunk_count must be positive

## Entity: UserQuery
**Description**: Represents a user's question along with context information (full-book vs selected text mode)
**Fields**:
- id: UUID (Primary Key)
- session_id: UUID (Foreign Key to ChatSession)
- query_text: String (The actual user question)
- query_mode: Enum (Values: "full-book", "selected-text")
- selected_text: Text (Optional, when in selected-text mode)
- created_at: DateTime
- metadata: JSON (Additional query context)

**Validation Rules**:
- query_text is required
- query_mode must be one of the allowed values
- selected_text required when query_mode is "selected-text"

## Entity: RetrievedContext
**Description**: Represents the relevant book passages retrieved to answer a specific query
**Fields**:
- id: UUID (Primary Key)
- query_id: UUID (Foreign Key to UserQuery)
- content: Text (The retrieved book passage)
- source_location: String (Page number, section, or other location reference)
- relevance_score: Float (Similarity score from vector search)
- chunk_id: String (Identifier for the specific chunk in vector DB)

**Validation Rules**:
- relevance_score must be between 0 and 1
- content is required
- source_location provides citation information

## Entity: GeneratedResponse
**Description**: Represents the AI-generated answer with citations to book sections
**Fields**:
- id: UUID (Primary Key)
- query_id: UUID (Foreign Key to UserQuery)
- response_text: Text (The generated response)
- citations: JSON (List of source locations referenced in response)
- generated_at: DateTime
- metadata: JSON (Generation parameters, model used, etc.)

**Validation Rules**:
- response_text is required
- citations must reference valid source locations
- metadata must include model information

## Relationships
- ChatSession (1) ←→ (Many) UserQuery
- UserQuery (1) ←→ (Many) RetrievedContext
- UserQuery (1) ←→ (1) GeneratedResponse
- BookContent (1) ←→ (Many) RetrievedContext (via source_location)

## State Transitions
- ChatSession: active → inactive (when session expires or user ends)
- UserQuery: pending → processed → responded