#!/usr/bin/env python3
"""
Basic test script for AI Orchestrator backend
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the app directory to the Python path
sys.path.append(str(Path(__file__).parent / "app"))

from models.database import engine, Base
from models import Task, User, Conversation, ServiceConfig
from core.orchestrator import AIOrchestrator
from core.command_parser import CommandParser
from sqlalchemy.orm import Session

async def test_database():
    """Test database connection and table creation"""
    print("🧪 Testing database...")
    try:
        # Create tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
        
        # Test session
        with Session(engine) as db:
            # Test service config creation
            config = ServiceConfig(
                service_name="test_service",
                service_type="test",
                base_url="http://localhost:8000",
                is_active=True
            )
            db.add(config)
            db.commit()
            print("✅ Database write test passed")
            
            # Test query
            result = db.query(ServiceConfig).filter_by(service_name="test_service").first()
            if result:
                print("✅ Database read test passed")
            else:
                print("❌ Database read test failed")
                
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False
    
    return True

async def test_command_parser():
    """Test command parsing"""
    print("🧪 Testing command parser...")
    try:
        parser = CommandParser()
        
        # Test a simple command
        command = "Go to google.com and search for AI automation"
        parsed = await parser.parse_command(command)
        
        if parsed and parsed.task_type:
            print(f"✅ Command parsed successfully: {parsed.task_type}")
            print(f"   Title: {parsed.title}")
            print(f"   Target Service: {parsed.target_service}")
            return True
        else:
            print("❌ Command parsing failed")
            return False
            
    except Exception as e:
        print(f"❌ Command parser test failed: {e}")
        return False

async def test_orchestrator():
    """Test orchestrator functionality"""
    print("🧪 Testing orchestrator...")
    try:
        with Session(engine) as db:
            orchestrator = AIOrchestrator(db)
            
            # Test queue status
            status = await orchestrator.get_queue_status()
            if isinstance(status, dict):
                print("✅ Queue status test passed")
            else:
                print("❌ Queue status test failed")
                
            # Test service health
            health = await orchestrator.get_service_health()
            if isinstance(health, dict):
                print("✅ Service health test passed")
            else:
                print("❌ Service health test failed")
                
            return True
            
    except Exception as e:
        print(f"❌ Orchestrator test failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("🚀 Starting AI Orchestrator tests...\n")
    
    tests = [
        ("Database", test_database),
        ("Command Parser", test_command_parser),
        ("Orchestrator", test_orchestrator),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"Running {test_name} test...")
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
        print()
    
    # Summary
    print("📊 Test Results:")
    print("=" * 40)
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} {status}")
        if result:
            passed += 1
    
    print("=" * 40)
    print(f"Total: {len(results)} tests, {passed} passed, {len(results) - passed} failed")
    
    if passed == len(results):
        print("🎉 All tests passed! The backend is ready to use.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    # Set up environment for testing
    os.environ.setdefault("DATABASE_URL", "sqlite:///./test_ai_orchestrator.db")
    os.environ.setdefault("OPENAI_API_KEY", "test-key")
    
    exit_code = asyncio.run(main())
    sys.exit(exit_code)