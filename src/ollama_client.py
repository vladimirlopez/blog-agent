import json
import time
import uuid
from typing import Dict, Any, AsyncGenerator
import httpx
from fastapi import HTTPException
from .schemas import ChatCompletionRequest, ChatCompletionResponse, ChatCompletionChoice, ChatCompletionUsage, ChatMessage


class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.chat_endpoint = f"{base_url}/api/chat"
        
    async def chat_completion(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        """Send a chat completion request to Ollama and return the response."""
        
        # Convert messages to Ollama format
        ollama_messages = []
        for msg in request.messages:
            ollama_messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        # Prepare Ollama request
        ollama_request = {
            "model": request.model,
            "messages": ollama_messages,
            "stream": False,
            "options": {}
        }
        
        # Add optional parameters
        if request.temperature is not None:
            ollama_request["options"]["temperature"] = request.temperature
        if request.max_tokens is not None:
            ollama_request["options"]["num_predict"] = request.max_tokens
        if request.stop is not None:
            ollama_request["options"]["stop"] = request.stop
        
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    self.chat_endpoint,
                    json=ollama_request
                )
                
                if response.status_code != 200:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"Ollama API error: {response.text}"
                    )
                
                ollama_response = response.json()
                
                # Convert Ollama response to OpenAI format
                completion_id = f"chatcmpl-{uuid.uuid4().hex}"
                created_timestamp = int(time.time())
                
                choice = ChatCompletionChoice(
                    index=0,
                    message=ChatMessage(
                        role=ollama_response["message"]["role"],
                        content=ollama_response["message"]["content"]
                    ),
                    finish_reason="stop"
                )
                
                # Calculate token usage (approximate)
                prompt_tokens = sum(len(msg.content.split()) for msg in request.messages)
                completion_tokens = len(ollama_response["message"]["content"].split())
                
                usage = ChatCompletionUsage(
                    prompt_tokens=prompt_tokens,
                    completion_tokens=completion_tokens,
                    total_tokens=prompt_tokens + completion_tokens
                )
                
                return ChatCompletionResponse(
                    id=completion_id,
                    created=created_timestamp,
                    model=request.model,
                    choices=[choice],
                    usage=usage
                )
                
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Failed to connect to Ollama: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error: {str(e)}"
            )
    
    async def list_models(self) -> Dict[str, Any]:
        """List available models from Ollama."""
        models_endpoint = f"{self.base_url}/api/tags"
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(models_endpoint)
                
                if response.status_code != 200:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"Ollama API error: {response.text}"
                    )
                
                return response.json()
                
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Failed to connect to Ollama: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error: {str(e)}"
            )

    async def stream_chat_completion(self, request: ChatCompletionRequest) -> AsyncGenerator[str, None]:
        """Stream a chat completion response from Ollama."""
        
        # Convert messages to Ollama format
        ollama_messages = []
        for msg in request.messages:
            ollama_messages.append({
                "role": msg.role,
                "content": msg.content
            })
        
        # Prepare Ollama request
        ollama_request = {
            "model": request.model,
            "messages": ollama_messages,
            "stream": True,
            "options": {}
        }
        
        # Add optional parameters
        if request.temperature is not None:
            ollama_request["options"]["temperature"] = request.temperature
        if request.max_tokens is not None:
            ollama_request["options"]["num_predict"] = request.max_tokens
        if request.stop is not None:
            ollama_request["options"]["stop"] = request.stop
        
        completion_id = f"chatcmpl-{uuid.uuid4().hex}"
        created_timestamp = int(time.time())
        
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                async with client.stream(
                    "POST",
                    self.chat_endpoint,
                    json=ollama_request
                ) as response:
                    if response.status_code != 200:
                        raise HTTPException(
                            status_code=response.status_code,
                            detail=f"Ollama API error: {response.text}"
                        )
                    
                    async for line in response.aiter_lines():
                        if line.strip():
                            try:
                                ollama_chunk = json.loads(line)
                                
                                # Convert to OpenAI streaming format
                                if ollama_chunk.get("message", {}).get("content"):
                                    chunk_data = {
                                        "id": completion_id,
                                        "object": "chat.completion.chunk",
                                        "created": created_timestamp,
                                        "model": request.model,
                                        "choices": [{
                                            "index": 0,
                                            "delta": {
                                                "content": ollama_chunk["message"]["content"]
                                            },
                                            "finish_reason": None
                                        }]
                                    }
                                    yield f"data: {json.dumps(chunk_data)}\n\n"
                                
                                # Send final chunk if done
                                if ollama_chunk.get("done", False):
                                    final_chunk = {
                                        "id": completion_id,
                                        "object": "chat.completion.chunk",
                                        "created": created_timestamp,
                                        "model": request.model,
                                        "choices": [{
                                            "index": 0,
                                            "delta": {},
                                            "finish_reason": "stop"
                                        }]
                                    }
                                    yield f"data: {json.dumps(final_chunk)}\n\n"
                                    yield "data: [DONE]\n\n"
                                    break
                                    
                            except json.JSONDecodeError:
                                continue
                                
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=503,
                detail=f"Failed to connect to Ollama: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error: {str(e)}"
            )
