#!/usr/bin/env python3
"""
Enhanced test script for the blog-agent project
Tests the draft_post endpoint with content validation
"""

import asyncio
import httpx
import json
from pathlib import Path


async def test_enhanced_draft_post():
    """Test the enhanced draft_post endpoint with content validation"""
    
    print("🚀 Testing Enhanced /tool/draft_post endpoint")
    print("=" * 60)
    
    # Test various topics with different complexity levels
    test_requests = [
        {
            "topic": "Getting Started with Python FastAPI",
            "model": "mistral:7b",
            "description": "Basic tutorial topic - should pass validation"
        },
        {
            "topic": "AI",
            "model": "mistral:7b", 
            "description": "Very short topic - may have content issues"
        },
        {
            "topic": "Advanced Machine Learning Techniques for Real-World Applications: A Comprehensive Deep Dive",
            "model": "mistral:7b",
            "description": "Complex topic - should generate comprehensive content"
        }
    ]
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        for i, request_data in enumerate(test_requests, 1):
            print(f"\n📝 Test {i}: {request_data['topic']}")
            print(f"   Description: {request_data['description']}")
            print("-" * 50)
            
            try:
                # Remove description from request (not part of API)
                api_request = {k: v for k, v in request_data.items() if k != 'description'}
                
                response = await client.post(
                    "http://localhost:4891/tool/draft_post",
                    json=api_request
                )
                
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ Success!")
                    print(f"   📄 File: {result['filename']}")
                    print(f"   📊 Word Count: {result.get('word_count', 'N/A')}")
                    
                    # Display content statistics
                    stats = result.get('content_stats', {})
                    if stats:
                        print(f"   📈 Content Stats:")
                        print(f"      - Headings: {stats.get('heading_count', 0)}")
                        print(f"      - Paragraphs: {stats.get('paragraph_count', 0)}")
                        print(f"      - Code blocks: {stats.get('code_blocks', 0)}")
                        print(f"      - Links: {stats.get('links', 0)}")
                        print(f"      - Images: {stats.get('images', 0)}")
                        print(f"      - Est. reading time: {stats.get('estimated_reading_time', 0)} min")
                    
                    # Display content issues if any
                    issues = result.get('content_issues')
                    if issues:
                        print(f"   ⚠️  Content Issues:")
                        for issue in issues:
                            print(f"      - {issue}")
                    else:
                        print(f"   ✅ No content issues detected")
                    
                    print(f"   👀 Preview: {result['preview'][:100]}...")
                    
                    # Verify file exists
                    file_path = Path(result['full_path'])
                    if file_path.exists():
                        print(f"   ✅ File created successfully at: {file_path}")
                    else:
                        print(f"   ❌ File not found at: {file_path}")
                    
                else:
                    print(f"❌ Error {response.status_code}: {response.text}")
                    
            except Exception as e:
                print(f"❌ Exception: {str(e)}")
            
            print()


async def test_model_validation():
    """Test model validation functionality"""
    print("\n🔍 Testing Model Validation")
    print("=" * 40)
    
    # Test with invalid model
    invalid_request = {
        "topic": "Test with invalid model",
        "model": "nonexistent-model"
    }
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(
                "http://localhost:4891/tool/draft_post",
                json=invalid_request
            )
            
            if response.status_code == 400:
                print("✅ Model validation working correctly")
                print(f"   Error message: {response.json()['detail']}")
            else:
                print(f"❌ Expected 400 error, got {response.status_code}")
                print(f"   Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Exception during model validation test: {str(e)}")


async def test_health_check():
    """Test basic health check"""
    print("\n🏥 Testing Health Check")
    print("=" * 30)
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            response = await client.get("http://localhost:4891/health")
            
            if response.status_code == 200:
                print("✅ Health check passed")
                print(f"   Response: {response.json()}")
            else:
                print(f"❌ Health check failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Exception during health check: {str(e)}")


async def main():
    """Run all tests"""
    print("🧪 BLOG-AGENT ENHANCED TESTING SUITE")
    print("=" * 70)
    
    await test_health_check()
    await test_enhanced_draft_post()
    await test_model_validation()
    
    print("\n🎉 Testing Complete!")
    print("=" * 70)
    print("Check the 'posts/' directory for generated files.")


if __name__ == "__main__":
    asyncio.run(main())
