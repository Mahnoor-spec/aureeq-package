@echo off
echo Starting Aureeq Services...

echo Starting TTS Service (Port 8880)...
start "Aureeq TTS" cmd /k "cd /d %~dp0 && set PYTHONPATH=%~dp0 && cd model_training\kokoro_tts && uvicorn main:app --host 0.0.0.0 --port 8880"

timeout /t 5

echo Starting Backend Service (Port 8001)...
start "Aureeq Backend" cmd /k "cd /d %~dp0 && set PYTHONPATH=%~dp0\model_training\scripts && set OLLAMA_HOST=http://localhost:11434 && call .venv\Scripts\activate && cd model_training\scripts && uvicorn server:app --host 127.0.0.1 --port 8001 --reload"

timeout /t 5

echo Starting Frontend Service (Port 5173)...
start "Aureeq Frontend" cmd /k "cd /d %~dp0\frontend && npm run dev"

echo All services started!
pause
