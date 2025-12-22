@echo off
echo Starting FastAPI application using local virtual environment...

REM Use the python interpreter from the .venv directory
".\.venv\Scripts\python.exe" -m uvicorn backend.src.api.main:app --reload --host 0.0.0.0 --port 8000

pause