import asyncio
import httpx
from schemas import ChatCompletionRequest, ChatMessage


async def test_chat_completion():
    """Test the chat completion endpoint."""
    
    # Test data
    test_request = {
        "model": "llama2",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Say hello!"}
        ],
        "temperature": 0.7,
        "max_tokens": 50
    }
    
    async with httpx.AsyncClient() as client:
        try:
            # Test non-streaming
            print("Testing non-streaming chat completion...")
            response = await client.post(
                "http://localhost:8000/v1/chat/completions",
                json=test_request,
                timeout=30.0
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Non-streaming test passed!")
                print(f"Response: {result['choices'][0]['message']['content']}")
                print(f"Usage: {result['usage']}")
            else:
                print(f"❌ Non-streaming test failed: {response.status_code}")
                print(f"Error: {response.text}")
            
            print("\n" + "="*50 + "\n")
            
            # Test streaming
            print("Testing streaming chat completion...")
            test_request["stream"] = True
            
            async with client.stream(
                "POST",
                "http://localhost:8000/v1/chat/completions",
                json=test_request,
                timeout=30.0
            ) as stream_response:
                if stream_response.status_code == 200:
                    print("✅ Streaming test started...")
                    print("Streaming response:")
                    async for line in stream_response.aiter_lines():
                        if line.strip() and line.startswith("data: "):
                            data = line[6:]  # Remove "data: " prefix
                            if data != "[DONE]":
                                print(f"Chunk: {data}")
                            else:
                                print("✅ Streaming completed!")
                else:
                    print(f"❌ Streaming test failed: {stream_response.status_code}")
                    print(f"Error: {await stream_response.aread()}")
                    
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")


async def test_health():
    """Test the health endpoint."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("http://localhost:8000/health")
            if response.status_code == 200:
                print("✅ Health check passed!")
                print(f"Response: {response.json()}")
            else:
                print(f"❌ Health check failed: {response.status_code}")
        except Exception as e:
            print(f"❌ Health check failed with exception: {e}")


async def main():
    """Run all tests."""
    print("🧪 Starting API tests...\n")
    
    await test_health()
    print("\n" + "="*50 + "\n")
    await test_chat_completion()
    
    print("\n🎉 Tests completed!")


if __name__ == "__main__":
    print("🧪 To run this test, use: uv run python test_api.py")
    print("Make sure the server is running with: uv run python main.py")
    print()
    asyncio.run(main())
