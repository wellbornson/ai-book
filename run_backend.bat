@echo off
echo Starting FastAPI application using local virtual environment...

REM Set database to SQLite for local development
set APP_DATABASE_URL=sqlite+aiosqlite:///./book_chatbot.db

REM Force in-memory Qdrant to avoid connection issues with blocked/incorrect cloud URL
set QDRANT_URL=your_qdrant_url_here

REM Use the python interpreter from the .venv directory
".\.venv\Scripts\python.exe" -m uvicorn backend.src.api.main:app --reload --host 0.0.0.0 --port 8000

pause