#!/usr/bin/env python3
import asyncio
import httpx
import sys

async def test_health():
    """Test the health endpoint"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get('http://localhost:8000/health')
            print(f"Health check: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"Response: {data}")
                return True
            else:
                print(f"Error: {response.text}")
                return False
    except Exception as e:
        print(f"Error testing health endpoint: {e}")
        return False

async def test_api_docs():
    """Test the API docs endpoint"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get('http://localhost:8000/docs')
            print(f"API docs: {response.status_code}")
            return response.status_code == 200
    except Exception as e:
        print(f"Error testing API docs: {e}")
        return False

async def main():
    """Run all tests"""
    print("Testing AI Orchestrator application...")
    
    # Test health endpoint
    health_ok = await test_health()
    
    # Test API docs
    docs_ok = await test_api_docs()
    
    if health_ok and docs_ok:
        print("✅ All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)