from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from schemas import ChatCompletionRequest, ChatCompletionResponse
from ollama_client import OllamaClient

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Ollama Chat API",
    description="A FastAPI service that provides OpenAI-compatible chat completions using Ollama",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Ollama client
ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
ollama_client = OllamaClient(base_url=ollama_base_url)


@app.get("/")
async def root():
    """Root endpoint with basic information."""
    return {
        "message": "Ollama Chat API",
        "version": "1.0.0",
        "endpoints": {
            "chat_completions": "/v1/chat/completions",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "ollama_url": ollama_base_url}


@app.post("/v1/chat/completions", response_model=ChatCompletionResponse)
async def chat_completions(request: ChatCompletionRequest):
    """
    Create a chat completion using Ollama.
    
    This endpoint mimics the OpenAI chat completions API and forwards
    requests to a local Ollama instance.
    """
    try:
        if request.stream:
            # Return streaming response
            return StreamingResponse(
                ollama_client.stream_chat_completion(request),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "Content-Type": "text/event-stream"
                }
            )
        else:
            # Return standard response
            return await ollama_client.chat_completion(request)
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process chat completion: {str(e)}"
        )


@app.get("/v1/models")
async def list_models():
    """
    List available models (placeholder implementation).
    
    In a real implementation, this would query Ollama for available models.
    """
    return {
        "object": "list",
        "data": [
            {
                "id": "llama2",
                "object": "model",
                "created": 1677610602,
                "owned_by": "ollama"
            },
            {
                "id": "codellama",
                "object": "model", 
                "created": 1677610602,
                "owned_by": "ollama"
            },
            {
                "id": "mistral",
                "object": "model",
                "created": 1677610602,
                "owned_by": "ollama"
            }
        ]
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 4891))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )
