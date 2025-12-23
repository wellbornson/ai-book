@echo off
echo Starting Backend Server...
start "Backend Server" cmd /k "run_backend.bat"

echo Waiting for backend to initialize...
timeout /t 5 /nobreak >nul

echo Starting Frontend...
cd rag-chat-bot
call npm install
npm run start
pause