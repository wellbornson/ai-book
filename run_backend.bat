@echo off
echo Installing/upgrading necessary Python packages...
pip install fastapi uvicorn

echo Starting FastAPI application...
uvicorn backend.src.api.main:app --reload --host 0.0.0.0 --port 8000

pause