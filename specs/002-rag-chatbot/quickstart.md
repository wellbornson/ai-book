# Quickstart Guide: RAG Chatbot for Published Book

## Prerequisites

- Python 3.11+
- Docker (optional, for containerized deployment)
- Cohere API key
- Qdrant Cloud account and API key
- Neon Serverless Postgres account and connection string

## Environment Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create environment file:
   ```bash
   cp .env.example .env
   ```

5. Update `.env` with your credentials:
   ```env
   COHERE_API_KEY=your_cohere_api_key
   QDRANT_URL=your_qdrant_url
   QDRANT_API_KEY=your_qdrant_api_key
   DATABASE_URL=your_neon_postgres_connection_string
   ```

## Running Locally

1. Start the application:
   ```bash
   uvicorn backend.src.api.main:app --reload --port 8000
   ```

2. The API will be available at `http://localhost:8000`

3. API documentation available at `http://localhost:8000/docs`

## Docker Deployment

1. Build the Docker image:
   ```bash
   docker build -t rag-chatbot .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 -e COHERE_API_KEY=your_key -e QDRANT_URL=your_url -e QDRANT_API_KEY=your_key -e DATABASE_URL=your_db_url rag-chatbot
   ```

## Getting Started with the API

### 1. Ingest a Book
```bash
curl -X POST http://localhost:8000/api/v1/books/ingest \
  -H "Authorization: Bearer your-token" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Sample Book",
    "author": "Author Name",
    "content": "Full text content of the book...",
    "format": "txt"
  }'
```

### 2. Create a Session
```bash
curl -X POST http://localhost:8000/api/v1/sessions \
  -H "Authorization: Bearer your-token" \
  -H "Content-Type: application/json" \
  -d '{
    "book_id": "book-uuid",
    "initial_context": "full-book"
  }'
```

### 3. Query the Book
```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Authorization: Bearer your-token" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "session-uuid",
    "query_text": "What is the main theme of this book?",
    "query_mode": "full-book"
  }'
```

## Testing

Run unit tests:
```bash
pytest tests/unit/
```

Run integration tests:
```bash
pytest tests/integration/
```

Run all tests:
```bash
pytest
```

## Configuration

The application can be configured through environment variables:

- `COHERE_API_KEY`: Your Cohere API key
- `QDRANT_URL`: Qdrant Cloud endpoint
- `QDRANT_API_KEY`: Qdrant API key
- `DATABASE_URL`: Neon Postgres connection string
- `ENVIRONMENT`: Set to "development", "staging", or "production"
- `DEBUG`: Enable/disable debug mode
- `MAX_TOKENS`: Maximum tokens for chunking (default: 1000)
- `CHUNK_OVERLAP`: Token overlap for chunking (default: 200)