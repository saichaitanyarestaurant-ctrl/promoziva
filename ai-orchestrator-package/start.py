#!/usr/bin/env python3
"""
AI Orchestrator - Startup Script
This script handles the complete startup process for the AI Orchestrator application.
"""

import os
import sys
import subprocess
import platform
import webbrowser
import time
from pathlib import Path

def print_banner():
    """Print the application banner"""
    print("=" * 60)
    print("🚀 AI Orchestrator - Starting Up")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is compatible"""
    print("📋 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print("❌ Python 3.11+ is required!")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    print("\n📦 Checking dependencies...")
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("   Please run: pip install -r backend/requirements.txt")
        return False

def setup_environment():
    """Setup environment variables and configuration"""
    print("\n⚙️  Setting up environment...")
    
    # Create .env file if it doesn't exist
    env_file = Path(".env")
    if not env_file.exists():
        print("📝 Creating .env file from template...")
        if Path(".env.example").exists():
            with open(".env.example", "r") as f:
                content = f.read()
            with open(".env", "w") as f:
                f.write(content)
            print("✅ .env file created")
            print("⚠️  Please edit .env file with your OpenRouter API key")
        else:
            print("❌ .env.example not found")
            return False
    else:
        print("✅ .env file exists")
    
    # Create necessary directories
    os.makedirs("backend/logs", exist_ok=True)
    os.makedirs("backend/data", exist_ok=True)
    print("✅ Directories created")
    
    return True

def check_openrouter_key():
    """Check if OpenRouter API key is configured"""
    print("\n🔑 Checking OpenRouter API key...")
    
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key or api_key == "your-openrouter-api-key-here":
        print("⚠️  OpenRouter API key not configured")
        print("   Please edit .env file and add your API key")
        print("   Get your key from: https://openrouter.ai")
        return False
    
    print("✅ OpenRouter API key configured")
    return True

def start_server():
    """Start the FastAPI server"""
    print("\n🚀 Starting AI Orchestrator server...")
    
    # Change to backend directory
    os.chdir("backend")
    
    # Start the server
    try:
        import uvicorn
        from main import app
        
        print("✅ Server starting on http://localhost:8000")
        print("   Press Ctrl+C to stop the server")
        print()
        
        # Open browser after a short delay
        def open_browser():
            time.sleep(3)
            try:
                webbrowser.open("http://localhost:8000")
            except:
                pass
        
        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # Start the server
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
        
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False
    
    return True

def main():
    """Main startup function"""
    print_banner()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        print("\n💡 To install dependencies, run:")
        print("   pip install -r backend/requirements.txt")
        sys.exit(1)
    
    # Setup environment
    if not setup_environment():
        sys.exit(1)
    
    # Check API key (warning only)
    check_openrouter_key()
    
    print("\n" + "=" * 60)
    print("🎉 AI Orchestrator is ready to start!")
    print("=" * 60)
    print()
    
    # Start the server
    start_server()

if __name__ == "__main__":
    main()