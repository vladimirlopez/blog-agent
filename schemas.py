from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str = Field(..., description="The role of the message sender (user, assistant, system)")
    content: str = Field(..., description="The content of the message")


class ChatCompletionRequest(BaseModel):
    model: str = Field(..., description="The model to use for completion")
    messages: List[ChatMessage] = Field(..., description="List of chat messages")
    temperature: Optional[float] = Field(0.7, ge=0, le=2, description="Sampling temperature")
    max_tokens: Optional[int] = Field(None, ge=1, description="Maximum number of tokens to generate")
    stream: Optional[bool] = Field(False, description="Whether to stream the response")
    stop: Optional[List[str]] = Field(None, description="Stop sequences")


class ChatCompletionChoice(BaseModel):
    index: int
    message: ChatMessage
    finish_reason: Optional[str] = None


class ChatCompletionUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[ChatCompletionChoice]
    usage: ChatCompletionUsage


class StreamingChatCompletionChunk(BaseModel):
    id: str
    object: str = "chat.completion.chunk"
    created: int
    model: str
    choices: List[Dict[str, Any]]


# Blog post schemas
class DraftPostRequest(BaseModel):
    topic: str = Field(..., description="The topic for the blog post draft")
    model: Optional[str] = Field("mistral:7b", description="The model to use for generation")
    blog_folder: Optional[str] = Field("posts", description="Target folder for blog posts")


class DraftPostResponse(BaseModel):
    """Response model for draft post creation."""
    filename: str = Field(..., description="The filename of the created draft")
    preview: str = Field(..., description="Preview of the first 200 characters")
    full_path: str = Field(..., description="Full path to the created file")
    status: str = Field("success", description="Status of the operation")
    word_count: Optional[int] = None
    content_stats: Optional[dict] = None
    content_issues: Optional[List[str]] = None
