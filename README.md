# Integrated RAG Chatbot for Published Book

This project implements an AI-powered chatbot that enables users to interact with published book content using Retrieval-Augmented Generation (RAG).

## Overview

The Integrated RAG Chatbot allows users to:
- Query full book content with accurate, cited responses
- Focus queries on user-selected text only
- Get responses powered exclusively by Cohere's API
- Experience fast, scalable, and maintainable interactions

## Core Features

- **Accurate Responses**: All answers are grounded in retrieved contexts from the book with citations
- **Dual Mode Operation**: Support for both full-book queries and user-selected text only mode
- **Cohere API Exclusivity**: Using Cohere's embed-english-v3.0/embed-multilingual-v3.0 and Command R/R+ models
- **Scalable Architecture**: Built with FastAPI, Qdrant Cloud, and Neon Serverless Postgres
- **Efficient Processing**: Optimized for large book content with proper chunking and overlap

## Technology Stack

- **Backend**: FastAPI with async endpoints
- **Embeddings**: Cohere embed-english-v3.0 or embed-multilingual-v3.0
- **Generation**: Cohere Command R or R+ model with streaming
- **Vector Database**: Qdrant Cloud (free tier)
- **Relational DB**: Neon Serverless Postgres
- **Orchestration**: LangChain for RAG chains and document loaders
- **Code Style**: Python 3.11+, type hints, black formatting

## Getting Started

### Prerequisites

- Python 3.11+
- Docker (optional, for containerized deployment)
- Cohere API key
- Qdrant Cloud account and API key
- Neon Serverless Postgres account and connection string

### Installation

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

### Running the Application

1. Start the application:
   ```bash
   uvicorn backend.src.api.main:app --reload --port 8000
   ```

2. The API will be available at `http://localhost:8000`

3. API documentation available at `http://localhost:8000/docs`

## API Endpoints

### Book Ingestion
- `POST /api/v1/books/ingest` - Ingest a book for RAG processing

### Chat Session Management
- `POST /api/v1/sessions` - Create a new chat session
- `GET /api/v1/sessions/{session_id}` - Get session details
- `GET /api/v1/sessions/{session_id}/history` - Get chat history for a session

### Query Processing
- `POST /api/v1/query` - Submit a query about the book content
- `POST /api/v1/sessions/{session_id}/select-text` - Update session to use selected text mode

## Project Constitution

This project follows the principles outlined in the [Project Constitution](.specify/memory/constitution.md).
"# book-chatbot" 
