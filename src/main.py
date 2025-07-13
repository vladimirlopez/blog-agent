from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import re
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from .schemas import ChatCompletionRequest, ChatCompletionResponse, DraftPostRequest, DraftPostResponse
from .ollama_client import OllamaClient
from .content_validator import ContentValidator

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

# Mount static files for web interface
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    """Root endpoint with basic information."""
    return {
        "message": "Ollama Chat API with Blog Agent",
        "version": "1.0.0",
        "endpoints": {
            "chat_completions": "/v1/chat/completions",
            "draft_post": "/tool/draft_post",
            "web_interface": "/static/index.html",
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


@app.post("/tool/draft_post", response_model=DraftPostResponse)
async def draft_blog_post(request: DraftPostRequest):
    """
    Generate a Quarto blog post draft using Ollama.
    
    Creates a .qmd file with YAML frontmatter and markdown content
    based on the provided topic.
    """
    try:
        # Validate that the requested model is available
        try:
            available_models = await ollama_client.list_models()
            model_names = [model.get('name', '') for model in available_models.get('models', [])]
            if request.model not in model_names:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Model '{request.model}' is not available. Available models: {', '.join(model_names)}"
                )
        except Exception as e:
            # If we can't validate models, log a warning but continue
            print(f"Warning: Could not validate model availability: {e}")
        
        # Create blog folder if it doesn't exist
        blog_folder = Path(request.blog_folder)
        blog_folder.mkdir(parents=True, exist_ok=True)
        
        # Generate slug from topic
        slug = re.sub(r'[^a-zA-Z0-9\s-]', '', request.topic.lower())
        slug = re.sub(r'\s+', '-', slug.strip())
        slug = slug[:50]  # Limit length
        
        # Create filename with date
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"{date_str}-{slug}.qmd"
        full_path = blog_folder / filename
        
        # Check if file already exists and create unique name if needed
        counter = 1
        original_filename = filename
        while full_path.exists():
            name_part = original_filename.replace('.qmd', '')
            filename = f"{name_part}-{counter}.qmd"
            full_path = blog_folder / filename
            counter += 1
        
        # Generate content using Ollama
        prompt = f"""Create a comprehensive Quarto blog post about "{request.topic}". 

Structure the post with:
1. YAML frontmatter including title, description, author, date, categories
2. Introduction paragraph
3. Main content with headings and subheadings
4. Code examples if relevant
5. Conclusion

Make it engaging and informative. Use proper Quarto markdown formatting.

Topic: {request.topic}"""
        
        # Use ollama_client to generate content
        chat_request = ChatCompletionRequest(
            model=request.model,
            messages=[
                {"role": "system", "content": "You are an expert technical writer who creates engaging blog posts in Quarto format. Start directly with the main content - do NOT include YAML frontmatter as it will be added automatically."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        # Generate the blog post content
        response = await ollama_client.chat_completion(chat_request)
        generated_content = response.choices[0].message.content
        
        # Remove any YAML frontmatter if it was generated
        lines = generated_content.split('\n')
        content_start = 0
        if lines[0].strip() == "---":
            for i, line in enumerate(lines[1:], 1):
                if line.strip() == "---":
                    content_start = i + 1
                    break
        
        main_content = '\n'.join(lines[content_start:]).strip()
        
        # Add proper Quarto frontmatter
        frontmatter = f"""---
title: "{request.topic}"
description: "A comprehensive guide to {request.topic.lower()}"
author: "AI Assistant"
date: "{datetime.now().strftime('%Y-%m-%d')}"
categories: [blog, ai, guide]
---

"""
        
        content = frontmatter + main_content
        
        # Validate content quality
        content_stats = ContentValidator.get_content_stats(content)
        is_valid, content_issues = ContentValidator.validate_content(content)
        
        # Write to file
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Create preview (first 200 chars of content, excluding frontmatter)
        content_lines = content.split('\n')
        content_start = 0
        for i, line in enumerate(content_lines):
            if line.strip() == "---" and i > 0:
                content_start = i + 1
                break
        
        content_preview = '\n'.join(content_lines[content_start:])
        preview = content_preview[:200] + "..." if len(content_preview) > 200 else content_preview
        preview = preview.strip()
        
        return DraftPostResponse(
            filename=filename,
            preview=preview,
            full_path=str(full_path.absolute()),
            status="success",
            word_count=content_stats['word_count'],
            content_stats=content_stats,
            content_issues=content_issues if content_issues else None
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create blog post draft: {str(e)}")


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


# Mount static files for the web interface
app.mount("/static", StaticFiles(directory="static"), name="static")


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 4891))
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )
