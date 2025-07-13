#!/usr/bin/env python3
"""
Quick Test Script for Ollama Chat API
Runs basic tests to verify the API is working correctly
"""

import asyncio
import httpx
import json
import sys
import time
from typing import Optional


class QuickTester:
    def __init__(self, base_url: str = "http://localhost:4891"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)
        self.passed = 0
        self.failed = 0
    
    def print_test(self, test_name: str, status: str, message: str = ""):
        """Print test result with formatting"""
        status_emoji = "✅" if status == "PASS" else "❌"
        print(f"{status_emoji} {test_name}: {status}")
        if message:
            print(f"   {message}")
        print()
    
    async def test_health(self) -> bool:
        """Test health endpoint"""
        try:
            response = await self.client.get(f"{self.base_url}/health")
            if response.status_code == 200:
                data = response.json()
                self.print_test("Health Check", "PASS", f"Status: {data.get('status')}")
                self.passed += 1
                return True
            else:
                self.print_test("Health Check", "FAIL", f"Status code: {response.status_code}")
                self.failed += 1
                return False
        except Exception as e:
            self.print_test("Health Check", "FAIL", f"Error: {str(e)}")
            self.failed += 1
            return False
    
    async def test_models(self) -> bool:
        """Test models endpoint"""
        try:
            response = await self.client.get(f"{self.base_url}/v1/models")
            if response.status_code == 200:
                data = response.json()
                models = [model["id"] for model in data.get("data", [])]
                self.print_test("List Models", "PASS", f"Models: {', '.join(models)}")
                self.passed += 1
                return True
            else:
                self.print_test("List Models", "FAIL", f"Status code: {response.status_code}")
                self.failed += 1
                return False
        except Exception as e:
            self.print_test("List Models", "FAIL", f"Error: {str(e)}")
            self.failed += 1
            return False
    
    async def test_chat_completion(self, model: str = "mistral:7b") -> bool:
        """Test basic chat completion"""
        try:
            payload = {
                "model": model,
                "messages": [
                    {"role": "user", "content": "Say 'Hello, testing!' and nothing else."}
                ],
                "max_tokens": 10
            }
            
            start_time = time.time()
            response = await self.client.post(
                f"{self.base_url}/v1/chat/completions",
                json=payload
            )
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                self.print_test(
                    "Chat Completion", 
                    "PASS", 
                    f"Response: {content[:50]}... (took {response_time:.2f}s)"
                )
                self.passed += 1
                return True
            else:
                self.print_test("Chat Completion", "FAIL", f"Status code: {response.status_code}")
                self.failed += 1
                return False
        except Exception as e:
            self.print_test("Chat Completion", "FAIL", f"Error: {str(e)}")
            self.failed += 1
            return False
    
    async def test_streaming(self, model: str = "mistral:7b") -> bool:
        """Test streaming chat completion"""
        try:
            payload = {
                "model": model,
                "messages": [
                    {"role": "user", "content": "Count: 1, 2, 3"}
                ],
                "max_tokens": 20,
                "stream": True
            }
            
            chunks_received = 0
            start_time = time.time()
            
            async with self.client.stream(
                "POST",
                f"{self.base_url}/v1/chat/completions",
                json=payload
            ) as response:
                if response.status_code == 200:
                    async for line in response.aiter_lines():
                        if line.strip() and line.startswith("data: "):
                            data_part = line[6:]  # Remove "data: " prefix
                            if data_part.strip() != "[DONE]":
                                chunks_received += 1
                            else:
                                break
                    
                    response_time = time.time() - start_time
                    self.print_test(
                        "Streaming Chat", 
                        "PASS", 
                        f"Received {chunks_received} chunks (took {response_time:.2f}s)"
                    )
                    self.passed += 1
                    return True
                else:
                    self.print_test("Streaming Chat", "FAIL", f"Status code: {response.status_code}")
                    self.failed += 1
                    return False
        except Exception as e:
            self.print_test("Streaming Chat", "FAIL", f"Error: {str(e)}")
            self.failed += 1
            return False
    
    async def test_error_handling(self) -> bool:
        """Test error handling with invalid model"""
        try:
            payload = {
                "model": "nonexistent-model",
                "messages": [
                    {"role": "user", "content": "test"}
                ]
            }
            
            response = await self.client.post(
                f"{self.base_url}/v1/chat/completions",
                json=payload
            )
            
            # We expect this to fail gracefully
            if response.status_code >= 400:
                self.print_test("Error Handling", "PASS", "Invalid model handled correctly")
                self.passed += 1
                return True
            else:
                self.print_test("Error Handling", "FAIL", "Should have failed with invalid model")
                self.failed += 1
                return False
        except Exception as e:
            self.print_test("Error Handling", "FAIL", f"Unexpected error: {str(e)}")
            self.failed += 1
            return False
    
    async def run_all_tests(self, model: str = "mistral:7b") -> None:
        """Run all tests"""
        print("🧪 Starting Quick Tests for Ollama Chat API")
        print(f"📍 Testing against: {self.base_url}")
        print(f"🤖 Using model: {model}")
        print("=" * 50)
        print()
        
        # Run tests in order
        await self.test_health()
        await self.test_models()
        await self.test_chat_completion(model)
        await self.test_streaming(model)
        await self.test_error_handling()
        
        # Summary
        total = self.passed + self.failed
        print("=" * 50)
        print(f"📊 Test Results: {self.passed}/{total} passed")
        
        if self.failed == 0:
            print("🎉 All tests passed! Your API is working correctly.")
        else:
            print(f"⚠️  {self.failed} test(s) failed. Check the logs above.")
        
        await self.client.aclose()
    
    async def check_prerequisites(self) -> bool:
        """Check if prerequisites are met"""
        print("🔍 Checking prerequisites...")
        
        # Check if server is running
        try:
            response = await self.client.get(f"{self.base_url}/", timeout=5.0)
            print("✅ FastAPI server is running")
        except Exception:
            print("❌ FastAPI server not responding")
            print(f"   Make sure the server is running on {self.base_url}")
            print("   Run: uv run python main.py")
            return False
        
        # Check if Ollama is running
        try:
            response = await self.client.get(f"{self.base_url}/health", timeout=5.0)
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "healthy":
                    print("✅ Ollama connection is healthy")
                    return True
                else:
                    print("❌ Ollama connection failed")
                    print("   Make sure Ollama is running: ollama serve")
                    return False
            else:
                print("❌ Health check failed")
                return False
        except Exception:
            print("❌ Cannot check Ollama status")
            return False


async def main():
    """Main test function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Quick test script for Ollama Chat API")
    parser.add_argument("--url", default="http://localhost:4891", help="API base URL")
    parser.add_argument("--model", default="mistral:7b", help="Model to test with")
    parser.add_argument("--skip-prereq", action="store_true", help="Skip prerequisite checks")
    
    args = parser.parse_args()
    
    tester = QuickTester(args.url)
    
    if not args.skip_prereq:
        if not await tester.check_prerequisites():
            print("\n❌ Prerequisites not met. Exiting.")
            await tester.client.aclose()
            sys.exit(1)
        print()
    
    await tester.run_all_tests(args.model)
    
    # Exit with error code if tests failed
    if tester.failed > 0:
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
