#!/bin/bash

echo "============================================================"
echo "🚀 AI Orchestrator - Starting Up (Unix/Linux/macOS)"
echo "============================================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed or not in PATH"
    echo "   Please install Python 3.11+ from https://python.org"
    exit 1
fi

echo "✅ Python found"
echo

# Check Python version
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
if [[ $(echo "$python_version >= 3.11" | bc -l 2>/dev/null) -eq 0 ]]; then
    echo "❌ Python 3.11+ is required. Current version: $python_version"
    echo "   Please upgrade Python from https://python.org"
    exit 1
fi

echo "✅ Python version $python_version - Compatible"
echo

# Check if virtual environment exists
if [ ! -d "backend/venv" ]; then
    echo "📦 Creating virtual environment..."
    cd backend
    python3 -m venv venv
    cd ..
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment exists"
fi

echo

# Activate virtual environment and install dependencies
echo "📦 Installing dependencies..."
cd backend
source venv/bin/activate
pip install -r requirements.txt
cd ..

echo

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "✅ .env file created"
    echo "⚠️  Please edit .env file with your OpenRouter API key"
    echo "   Get your key from: https://openrouter.ai"
else
    echo "✅ .env file exists"
fi

echo

# Create necessary directories
mkdir -p backend/logs
mkdir -p backend/data
echo "✅ Directories created"

echo

echo "============================================================"
echo "🎉 AI Orchestrator is ready to start!"
echo "============================================================"
echo

# Start the server
cd backend
source venv/bin/activate
echo "🚀 Starting server on http://localhost:8000"
echo "   Press Ctrl+C to stop the server"
echo
uvicorn main:app --host 0.0.0.0 --port 8000 --reload