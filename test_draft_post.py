#!/usr/bin/env python3
"""
Test script for the draft_post endpoint
"""

import asyncio
import httpx
import json


async def test_draft_post():
    """Test the draft_post endpoint"""
    
    print("🧪 Testing /tool/draft_post endpoint")
    print("=" * 50)
    
    # Test data
    test_requests = [
        {
            "topic": "Why I love teaching physics with AI",
            "model": "mistral:7b",
            "blog_folder": "posts"
        },
        {
            "topic": "Getting started with FastAPI and Ollama",
            "model": "mistral:7b"
        },
        {
            "topic": "Building MCP servers for VS Code integration"
        }
    ]
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        for i, request_data in enumerate(test_requests, 1):
            print(f"\n📝 Test {i}: {request_data['topic'][:50]}...")
            
            try:
                response = await client.post(
                    "http://localhost:4891/tool/draft_post",
                    json=request_data
                )
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ Success!")
                    print(f"   📄 File: {result['filename']}")
                    print(f"   📁 Path: {result['full_path']}")
                    print(f"   👀 Preview: {result['preview'][:100]}...")
                    
                else:
                    print(f"❌ Failed: {response.status_code}")
                    print(f"   Error: {response.text}")
                    
            except Exception as e:
                print(f"❌ Exception: {str(e)}")


async def test_mcp_draft_post():
    """Test the draft_post tool via MCP"""
    
    print("\n\n🔧 Testing draft_post via MCP protocol")
    print("=" * 50)
    
    import subprocess
    
    # Test MCP draft_post tool
    mcp_request = {
        "jsonrpc": "2.0", 
        "id": 4, 
        "method": "tools/call", 
        "params": {
            "name": "draft_post", 
            "arguments": {
                "topic": "Building AI-powered development tools with MCP",
                "model": "mistral:7b"
            }
        }
    }
    
    try:
        # Use subprocess to test MCP server
        process = subprocess.run(
            ["uv", "run", "python", "mcp_server.py"],
            input=json.dumps(mcp_request),
            text=True,
            capture_output=True,
            timeout=60
        )
        
        if process.returncode == 0:
            result = json.loads(process.stdout)
            print("✅ MCP test successful!")
            print(f"   Response: {result.get('result', {}).get('content', [{}])[0].get('text', 'No content')[:200]}...")
        else:
            print(f"❌ MCP test failed: {process.stderr}")
            
    except Exception as e:
        print(f"❌ MCP test exception: {str(e)}")


async def main():
    """Run all tests"""
    print("🚀 Starting draft_post tests...")
    
    # First test the direct API
    await test_draft_post()
    
    # Then test via MCP
    await test_mcp_draft_post()
    
    print("\n🎉 Tests completed!")


if __name__ == "__main__":
    asyncio.run(main())
