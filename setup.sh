#!/bin/bash

# AI Orchestrator Setup Script
echo "🚀 Setting up AI Orchestrator..."

# Check if Python 3.11+ is installed
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
if [[ $(echo "$python_version >= 3.11" | bc -l) -eq 0 ]]; then
    echo "❌ Python 3.11+ is required. Current version: $python_version"
    exit 1
fi

# Check if Node.js 18+ is installed
node_version=$(node --version 2>&1 | grep -oP '\d+' | head -1)
if [[ $node_version -lt 18 ]]; then
    echo "❌ Node.js 18+ is required. Current version: $node_version"
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is required but not installed."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is required but not installed."
    exit 1
fi

echo "✅ Prerequisites check passed!"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp backend/.env.example .env
    echo "⚠️  Please edit .env file with your API keys before running the application."
fi

# Create virtual environment for backend
echo "🐍 Setting up Python virtual environment..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd frontend/web
npm install
cd ../..

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p backend/logs
mkdir -p backend/screenshots
mkdir -p backend/data

echo "✅ Setup completed!"
echo ""
echo "📋 Next steps:"
echo "1. Edit the .env file with your API keys:"
echo "   - OPENAI_API_KEY"
echo "   - GOOGLE_CLIENT_ID (optional)"
echo "   - GOOGLE_CLIENT_SECRET (optional)"
echo "   - TWILIO_ACCOUNT_SID (optional)"
echo "   - TWILIO_AUTH_TOKEN (optional)"
echo "   - ELEVENLABS_API_KEY (optional)"
echo ""
echo "2. Run the application:"
echo "   Option A - Using Docker (recommended):"
echo "   docker-compose up -d"
echo ""
echo "   Option B - Local development:"
echo "   Backend: cd backend && source venv/bin/activate && uvicorn main:app --reload"
echo "   Frontend: cd frontend/web && npm run dev"
echo ""
echo "3. Access the application:"
echo "   - Web Dashboard: http://localhost:3000"
echo "   - API Documentation: http://localhost:8000/docs"
echo "   - API Health Check: http://localhost:8000/health"
echo ""
echo "🎉 Happy coding!"