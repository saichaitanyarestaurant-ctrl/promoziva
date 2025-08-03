@echo off
echo ============================================================
echo 🚀 AI Orchestrator - Starting Up (Windows)
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo    Please install Python 3.11+ from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Check if virtual environment exists
if not exist "backend\venv" (
    echo 📦 Creating virtual environment...
    cd backend
    python -m venv venv
    cd ..
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment exists
)

echo.

REM Activate virtual environment and install dependencies
echo 📦 Installing dependencies...
cd backend
call venv\Scripts\activate.bat
pip install -r requirements.txt
cd ..

echo.

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo 📝 Creating .env file...
    copy .env.example .env
    echo ✅ .env file created
    echo ⚠️  Please edit .env file with your OpenRouter API key
    echo    Get your key from: https://openrouter.ai
) else (
    echo ✅ .env file exists
)

echo.

REM Create necessary directories
if not exist "backend\logs" mkdir backend\logs
if not exist "backend\data" mkdir backend\data

echo.

echo ============================================================
echo 🎉 AI Orchestrator is ready to start!
echo ============================================================
echo.

REM Start the server
cd backend
call venv\Scripts\activate.bat
echo 🚀 Starting server on http://localhost:8000
echo    Press Ctrl+C to stop the server
echo.
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

pause