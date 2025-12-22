# API Contract: RAG Chatbot for Published Book

## Base URL
`/api/v1`

## Authentication
Bearer token authentication required for all endpoints

## Endpoints

### Book Ingestion

#### POST /books/ingest
**Description**: Ingest a book for RAG processing
**Request**:
```json
{
  "title": "string",
  "author": "string",
  "content": "string",
  "format": "pdf|txt|epub"
}
```
**Response (201 Created)**:
```json
{
  "book_id": "uuid",
  "title": "string",
  "status": "processing|completed",
  "message": "string"
}
```

#### GET /books/{book_id}
**Description**: Get book information
**Response (200 OK)**:
```json
{
  "id": "uuid",
  "title": "string",
  "author": "string",
  "chunk_count": "integer",
  "created_at": "datetime"
}
```

### Chat Session Management

#### POST /sessions
**Description**: Create a new chat session
**Request**:
```json
{
  "book_id": "uuid",
  "initial_context": "full-book|selected-text",
  "selected_text": "string (optional)"
}
```
**Response (201 Created)**:
```json
{
  "session_id": "uuid",
  "created_at": "datetime",
  "book_id": "uuid"
}
```

#### GET /sessions/{session_id}
**Description**: Get session details
**Response (200 OK)**:
```json
{
  "id": "uuid",
  "title": "string",
  "created_at": "datetime",
  "updated_at": "datetime",
  "book_id": "uuid"
}
```

#### GET /sessions/{session_id}/history
**Description**: Get chat history for a session
**Response (200 OK)**:
```json
[
  {
    "query": "string",
    "response": "string",
    "timestamp": "datetime",
    "citations": ["string"]
  }
]
```

### Query Processing

#### POST /query
**Description**: Submit a query about the book content
**Request**:
```json
{
  "session_id": "uuid",
  "query_text": "string",
  "query_mode": "full-book|selected-text",
  "selected_text": "string (optional)"
}
```
**Response (200 OK)**:
```json
{
  "response_id": "uuid",
  "response_text": "string",
  "citations": [
    {
      "source_location": "string",
      "content": "string"
    }
  ],
  "query_mode": "full-book|selected-text"
}
```

### Text Selection Mode

#### POST /sessions/{session_id}/select-text
**Description**: Update session to use selected text mode
**Request**:
```json
{
  "selected_text": "string"
}
```
**Response (200 OK)**:
```json
{
  "session_id": "uuid",
  "selected_text": "string",
  "query_mode": "selected-text"
}
```

## Error Responses

All error responses follow this format:
```json
{
  "error": {
    "code": "string",
    "message": "string",
    "details": "object (optional)"
  }
}
```

Common error codes:
- `VALIDATION_ERROR`: Request validation failed
- `NOT_FOUND`: Requested resource does not exist
- `PROCESSING_ERROR`: Error during content processing
- `EXTERNAL_SERVICE_ERROR`: Error with Cohere or vector database
- `UNAUTHORIZED`: Authentication required or failed