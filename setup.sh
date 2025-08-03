#!/bin/bash

# AI Orchestrator Setup Script
echo "🚀 Setting up AI Orchestrator..."

# Check if Python 3.11+ is installed
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
if [[ $(echo "$python_version >= 3.11" | bc -l 2>/dev/null) -eq 0 ]]; then
    echo "❌ Python 3.11+ is required. Current version: $python_version"
    echo "Please install Python 3.11 or higher from https://python.org"
    exit 1
fi

echo "✅ Python version check passed: $python_version"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your OpenRouter API key before running the application."
    echo "   Get your API key from: https://openrouter.ai"
fi

# Create virtual environment for backend
echo "🐍 Setting up Python virtual environment..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cd ..

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p backend/logs
mkdir -p backend/data

echo "✅ Setup completed!"
echo ""
echo "📋 Next steps:"
echo "1. Edit the .env file with your OpenRouter API key:"
echo "   - OPENROUTER_API_KEY=your-api-key-here"
echo "   - Get your API key from: https://openrouter.ai"
echo ""
echo "2. Run the application:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   uvicorn main:app --reload"
echo ""
echo "3. Access the application:"
echo "   - Web Interface: http://localhost:8000"
echo "   - API Documentation: http://localhost:8000/docs"
echo "   - Health Check: http://localhost:8000/health"
echo ""
echo "🎉 Happy coding!"