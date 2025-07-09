# Building a FastAPI + Ollama Chat API: A Complete Guide

*A step-by-step documentation of creating an OpenAI-compatible chat API using FastAPI and Ollama with modern Python tooling*

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Initial Setup and Architecture](#initial-setup-and-architecture)
3. [Implementation Details](#implementation-details)
4. [Migration to UV Package Manager](#migration-to-uv-package-manager)
5. [MCP Integration](#mcp-integration)
6. [Troubleshooting](#troubleshooting)
7. [Final Project Structure](#final-project-structure)
8. [Key Learnings](#key-learnings)

---

## Project Overview

### Goal
Create a FastAPI service that provides an OpenAI-compatible `/v1/chat/completions` endpoint that relays messages to a local Ollama model running at `http://localhost:11434`.

### Key Requirements
- OpenAI-compatible API format
- Support for both streaming and non-streaming responses
- Proper error handling and request validation
- Modern Python tooling and dependency management
- Comprehensive documentation and testing

### Technology Stack
- **FastAPI**: Modern, fast web framework for building APIs
- **Ollama**: Local LLM inference server
- **UV**: Fast Python package manager
- **Pydantic**: Data validation and serialization
- **HTTPX**: Async HTTP client for API calls

---

## Initial Setup and Architecture

### 1. Project Structure Design

The project was structured to be modular and maintainable:

```
blog-agent/
├── main.py              # FastAPI application entry point
├── schemas.py           # Pydantic models for request/response
├── ollama_client.py     # Client for Ollama API communication
├── test_api.py          # Testing utilities
├── pyproject.toml       # Project configuration
├── .env.example         # Environment configuration template
├── README.md            # User documentation
├── DEVELOPMENT.md       # Developer documentation
└── setup scripts        # Automated setup
```

### 2. Schema Design

**Key Design Decision**: Use Pydantic models to ensure type safety and automatic validation.

Created comprehensive schemas in `schemas.py`:

```python
class ChatMessage(BaseModel):
    role: str = Field(..., description="The role of the message sender")
    content: str = Field(..., description="The content of the message")

class ChatCompletionRequest(BaseModel):
    model: str = Field(..., description="The model to use for completion")
    messages: List[ChatMessage] = Field(..., description="List of chat messages")
    temperature: Optional[float] = Field(0.7, ge=0, le=2)
    max_tokens: Optional[int] = Field(None, ge=1)
    stream: Optional[bool] = Field(False)
    stop: Optional[List[str]] = Field(None)
```

**Why this approach?**
- Automatic request validation
- Clear API documentation
- Type safety throughout the application
- Easy serialization/deserialization

### 3. Ollama Client Implementation

**Challenge**: Convert between OpenAI and Ollama API formats seamlessly.

**Solution**: Created a dedicated `OllamaClient` class that:
- Handles format conversion automatically
- Supports both streaming and non-streaming responses
- Provides comprehensive error handling
- Estimates token usage for OpenAI compatibility

```python
class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.chat_endpoint = f"{base_url}/api/chat"
    
    async def chat_completion(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        # Convert OpenAI format to Ollama format
        # Make API call
        # Convert response back to OpenAI format
```

### 4. FastAPI Application Structure

**Key Features Implemented**:
- CORS middleware for web applications
- Comprehensive error handling
- Health check endpoint
- Model listing endpoint
- Interactive API documentation

```python
@app.post("/v1/chat/completions", response_model=ChatCompletionResponse)
async def chat_completions(request: ChatCompletionRequest):
    if request.stream:
        return StreamingResponse(...)
    else:
        return await ollama_client.chat_completion(request)
```

---

## Implementation Details

### 1. Request Flow

```
Client Request → FastAPI Validation → Format Conversion → Ollama API → Response Conversion → Client Response
```

### 2. Streaming Implementation

**Challenge**: Handle real-time streaming responses from Ollama.

**Solution**: 
- Use FastAPI's `StreamingResponse`
- Convert Ollama streaming format to OpenAI Server-Sent Events
- Proper chunk formatting with `data: ` prefix

```python
async def stream_chat_completion(self, request: ChatCompletionRequest):
    async with httpx.AsyncClient() as client:
        async with client.stream("POST", self.chat_endpoint, json=ollama_request) as response:
            async for line in response.aiter_lines():
                # Convert Ollama chunk to OpenAI format
                yield f"data: {json.dumps(chunk_data)}\n\n"
```

### 3. Error Handling Strategy

**Comprehensive Error Handling**:
- Connection errors to Ollama
- Invalid model requests
- Request validation errors
- Timeout handling

```python
try:
    async with httpx.AsyncClient(timeout=120.0) as client:
        # API call logic
except httpx.RequestError as e:
    raise HTTPException(status_code=503, detail=f"Failed to connect to Ollama: {str(e)}")
except Exception as e:
    raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
```

### 4. Testing Strategy

Created `test_api.py` with:
- Health check testing
- Non-streaming completion testing
- Streaming completion testing
- Error condition testing

---

## Migration to UV Package Manager

### Why UV?

**Traditional pip/requirements.txt limitations**:
- Slow dependency resolution
- Inconsistent virtual environment management
- No built-in lockfile support
- Limited project metadata handling

**UV advantages**:
- 10-100x faster than pip
- Built-in virtual environment management
- Consistent dependency resolution
- Modern Python project standards

### Migration Process

#### 1. Replace requirements.txt with pyproject.toml

**Before**:
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
httpx==0.25.2
pydantic==2.5.0
python-dotenv==1.0.0
```

**After**:
```toml
[project]
name = "ollama-chat-api"
version = "1.0.0"
description = "A FastAPI service that provides OpenAI-compatible chat completions using Ollama"
requires-python = ">=3.8.1"
dependencies = [
    "fastapi>=0.104.1",
    "uvicorn[standard]>=0.24.0",
    "httpx>=0.25.2",
    "pydantic>=2.5.0",
    "python-dotenv>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-asyncio>=0.21.0",
    "black>=23.0.0",
    "flake8>=6.0.0",
    "mypy>=1.0.0",
]
```

#### 2. Update All Scripts and Documentation

**Command Changes**:
- `pip install -r requirements.txt` → `uv sync`
- `python main.py` → `uv run python main.py`
- `pip install package` → `uv add package`

#### 3. Create Setup Scripts

**Windows PowerShell** (`setup.ps1`):
```powershell
# Check if uv is installed
try {
    $uvVersion = uv --version
    Write-Host "✅ uv is installed: $uvVersion"
} catch {
    Write-Host "❌ uv is not installed. Installing..."
    # Installation instructions
}

uv sync
```

**Unix/Linux/macOS** (`setup.sh`):
```bash
# Check if uv is installed
if command -v uv &> /dev/null; then
    echo "✅ uv is installed: $(uv --version)"
else
    echo "❌ uv is not installed. Installing..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

uv sync
```

---

## MCP Integration

### What is MCP?

**Model Context Protocol (MCP)** is a standardized protocol for connecting AI assistants to external tools and data sources. This allows VS Code and other compatible applications to interact with your local Ollama models through a unified interface.

### Why Add MCP Support?

**Integration Benefits**:
- **VS Code Integration**: Direct access to Ollama models from VS Code
- **Standardized Protocol**: Uses industry-standard JSON-RPC 2.0
- **Tool Ecosystem**: Compatible with other MCP-enabled applications
- **Development Workflow**: Seamless AI assistance during coding

### Implementation Approach

#### 1. Port Configuration

**Challenge**: MCP requires a specific port configuration for VS Code integration.

**Solution**: 
- Changed FastAPI server from port 8000 to 4891 (MCP compatible)
- Updated all documentation and examples
- Maintained backward compatibility

```python
# main.py - Updated port configuration
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 4891))  # Changed from 8000 to 4891
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )
```

#### 2. MCP Server Implementation

**Challenge**: Implement full MCP protocol support using JSON-RPC 2.0.

**Solution**: Created `mcp_server.py` with comprehensive protocol implementation:

```python
class MCPServer:
    """MCP Server for Ollama Chat API integration"""
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming MCP requests"""
        method = request.get("method")
        params = request.get("params", {})
        
        if method == "initialize":
            return await self._handle_initialize(request_id, params)
        elif method == "tools/list":
            return await self._handle_list_tools(request_id)
        elif method == "tools/call":
            return await self._handle_tool_call(request_id, params)
        # ... additional methods
```

**Key Features**:
- **JSON-RPC 2.0 Protocol**: Full compliance with MCP specification
- **Tool Management**: List and execute available tools
- **Resource Access**: Expose API endpoints as resources
- **Prompt Templates**: Pre-configured prompts for common use cases
- **Error Handling**: Comprehensive error management

#### 3. MCP Tools Implementation

**Available Tools**:

1. **`chat_completion`**:
   - Generate chat completions using Ollama models
   - Full parameter support (temperature, max_tokens, streaming)
   - Format conversion between OpenAI and Ollama

2. **`health_check`**:
   - Check API health status
   - Monitor Ollama connectivity
   - System status reporting

3. **`list_models`**:
   - List available Ollama models
   - Model capability information
   - Dynamic model discovery

#### 4. VS Code Integration

**Configuration Files**:

**`.vscode/settings.json`**:
```json
{
  "mcp.servers": {
    "ollama-chat-api": {
      "command": "uv",
      "args": ["run", "python", "mcp_server.py"],
      "cwd": "${workspaceFolder}",
      "env": {
        "OLLAMA_BASE_URL": "http://localhost:11434",
        "MCP_SERVER_PORT": "4891"
      }
    }
  },
  "mcp.enabled": true
}
```

**Launch Configurations**:
- Debug FastAPI server
- Debug MCP server
- Integrated development workflow

#### 5. MCP Manifest

**`mcp-manifest.json`**: Complete server configuration including:
- Server capabilities and metadata
- Tool definitions with input schemas
- Resource endpoint specifications
- Prompt template configurations
- Environment variable documentation

### Testing MCP Integration

**Protocol Testing**:
```bash
# Test MCP protocol directly
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}' | uv run python mcp_server.py
```

**VS Code Testing**:
1. Install MCP extension in VS Code
2. Start FastAPI server: `start_mcp.bat`
3. Start MCP server: `uv run python mcp_server.py`
4. Use VS Code's MCP tools panel

### MCP Development Workflow

**Development Process**:
1. **Start Services**: FastAPI server (4891) and MCP server
2. **VS Code Integration**: Automatic connection via MCP protocol
3. **Tool Usage**: Access Ollama models directly from VS Code
4. **Debugging**: Full debugging support for both servers

**Benefits for Development**:
- **Integrated AI**: Access to local models during coding
- **Context Awareness**: VS Code can provide project context to models
- **Seamless Workflow**: No need to switch between applications
- **Customizable**: Easy to add new tools and capabilities

---

## Troubleshooting

### Issue 1: Python Version Compatibility

**Problem**: 
```
× No solution found when resolving dependencies for split (python_full_version >= '3.8' and python_full_version < '3.8.1'):
╰─▶ Because the requested Python version (>=3.8) does not satisfy Python>=3.8.1 and flake8>=6.0.0,<=7.1.2 depends on Python>=3.8.1
```

**Root Cause**: 
The `requires-python = ">=3.8"` in `pyproject.toml` was too broad, as some dependencies (like flake8) require Python >=3.8.1.

**Solution**:
```toml
# Changed from:
requires-python = ">=3.8"

# To:
requires-python = ">=3.8.1"
```

### Issue 2: Build System Configuration

**Problem**:
```
ValueError: Unable to determine which files to ship inside the wheel using the following heuristics...
The most likely cause of this is that there is no directory that matches the name of your project (ollama_chat_api).
```

**Root Cause**:
The project included build system configuration (`build-system` and `project.scripts`) which is unnecessary for a simple script-based project that doesn't need to be built as a package.

**Solution**:
Removed the build system configuration from `pyproject.toml`:
```toml
# Removed these sections:
[project.scripts]
ollama-chat-api = "main:app"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

**Key Learning**: Only include build system configuration when you actually need to build and distribute a package.

### Issue 2: Virtual Environment Management

**UV automatically handles virtual environments**:
- Creates `.venv` directory automatically
- No need to manually activate/deactivate
- `uv run` automatically uses the project's virtual environment

### Issue 3: Dependency Resolution

**UV's dependency resolver is more strict than pip**:
- Catches version conflicts early
- Provides clear error messages
- Suggests solutions (like updating `requires-python`)

---

## Final Project Structure

```
blog-agent/
├── main.py                  # FastAPI application with all endpoints
├── schemas.py              # Pydantic models for type safety
├── ollama_client.py        # Ollama API client with format conversion
├── mcp_server.py           # MCP server implementation
├── test_api.py            # Comprehensive API testing
├── pyproject.toml         # Modern Python project configuration
├── mcp-manifest.json      # MCP server configuration
├── setup.ps1              # Windows automated setup
├── setup.sh               # Unix/Linux/macOS automated setup
├── start.bat              # Windows quick start script
├── start_mcp.bat          # Windows MCP-enabled start script
├── .env.example           # Environment configuration template
├── .gitignore             # Git ignore with UV-specific entries
├── .vscode/               # VS Code configuration
│   ├── settings.json      # MCP server configuration
│   ├── launch.json        # Debug configurations
│   └── tasks.json         # Build and run tasks
├── README.md              # User-facing documentation
├── DEVELOPMENT.md         # Developer commands reference
├── MCP_SETUP.md           # MCP integration guide
└── BLOG_DOCUMENTATION.md  # This file - complete process documentation
```

---

## Key Learnings

### 1. API Design Principles

**OpenAI Compatibility**: 
- Following established API patterns makes integration easier
- Proper error codes and response formats matter
- Documentation is crucial for API adoption

**Streaming vs Non-Streaming**:
- Different use cases require different approaches
- Streaming is essential for real-time applications
- Both modes should be supported for flexibility

### 2. Modern Python Tooling

**UV Benefits**:
- Significantly faster than traditional pip
- Better dependency resolution
- Built-in virtual environment management
- Modern project structure with pyproject.toml

**Migration Considerations**:
- Always check dependency compatibility
- Update all scripts and documentation
- Provide clear migration instructions

### 3. Error Handling Strategy

**Comprehensive Error Handling**:
- Network connectivity issues
- API response errors
- Validation failures
- Timeout scenarios

**User Experience**:
- Clear error messages
- Proper HTTP status codes
- Graceful degradation

### 4. Testing and Documentation

**Testing Strategy**:
- Unit tests for individual components
- Integration tests for full API flow
- Error condition testing
- Performance testing for streaming

**Documentation Approach**:
- User-focused README
- Developer-focused DEVELOPMENT.md
- API documentation via FastAPI's automatic docs
- Process documentation (this file)

---

## Performance Considerations

### 1. Async/Await Pattern

**All I/O operations are async**:
- FastAPI endpoints
- HTTPX client calls
- Streaming responses

**Benefits**:
- High concurrency
- Non-blocking operations
- Better resource utilization

### 2. Connection Management

**HTTPX Client**:
- Async context managers for proper resource cleanup
- Timeout configurations
- Connection pooling

### 3. Streaming Optimization

**Memory Efficient**:
- Process chunks as they arrive
- Don't buffer entire response
- Proper cleanup of resources

---

## Security Considerations

### 1. Input Validation

**Pydantic Models**:
- Automatic validation of all inputs
- Type checking
- Range validation (temperature, max_tokens)

### 2. Error Information

**Controlled Error Responses**:
- Don't expose internal details
- Consistent error format
- Appropriate HTTP status codes

### 3. Environment Configuration

**Environment Variables**:
- Sensitive configuration via .env files
- Default values for development
- Clear documentation of required variables

---

## Future Enhancements

### 1. Model Management

**Current**: Placeholder model listing
**Future**: Dynamic model discovery from Ollama

### 2. Authentication

**Current**: Open API
**Future**: API key authentication, rate limiting

### 3. Monitoring

**Current**: Basic health checks
**Future**: Metrics, logging, monitoring integration

### 4. Deployment

**Current**: Local development
**Future**: Docker containerization, cloud deployment

### 5. MCP Integration

**Current**: VS Code integration with JSON-RPC 2.0 protocol
**Future**: Support for additional MCP-compatible applications and tools

---

## Conclusion

This project successfully demonstrates:

1. **Modern API Development**: Using FastAPI for fast, type-safe API development
2. **Integration Patterns**: Seamless integration between different API formats
3. **Modern Tooling**: Migration to UV for better dependency management
4. **Protocol Implementation**: Full MCP support for VS Code integration
5. **Documentation**: Comprehensive documentation for both users and developers
6. **Testing**: Practical testing strategies for API services

The combination of FastAPI, Ollama, UV, and MCP provides a comprehensive foundation for building production-ready AI API services with modern Python tooling and seamless IDE integration.

---

*This documentation serves as a complete guide for building similar projects and understanding the decisions made throughout the development process.*
