# Ollama Chat API

A FastAPI service that provides OpenAI-compatible chat completions using Ollama.

This project uses [uv](https://docs.astral.sh/uv/) for fast, reliable Python package management.

## Quick Start

```bash
# 1. Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh  # macOS/Linux
# or
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"  # Windows

# 2. Setup project
uv sync

# 3. Run the server
uv run python main.py
```

## Features

- OpenAI-compatible `/v1/chat/completions` endpoint
- Streaming and non-streaming responses
- Automatic request/response format conversion
- CORS support
- Health check endpoint
- Model listing endpoint
- **MCP (Model Context Protocol) support** for VS Code integration

## Setup

1. Install uv (if not already installed):
```bash
# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# On macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Install dependencies and create virtual environment:
```bash
uv sync
```

3. Make sure Ollama is running locally on `http://localhost:11434`

4. (Optional) Create a `.env` file to customize the Ollama URL:
```env
OLLAMA_BASE_URL=http://localhost:11434
```

## Running the Server

```bash
uv run python main.py
```

Or with uvicorn directly:
```bash
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:4891` (MCP compatible port)

## MCP (Model Context Protocol) Integration

This project includes MCP support for VS Code integration. See [MCP_SETUP.md](MCP_SETUP.md) for detailed setup instructions.

**Quick MCP Setup:**
1. Install MCP extension in VS Code
2. Run `start_mcp.bat` to start the server on port 4891
3. In a separate terminal: `uv run python mcp_server.py`
4. VS Code will automatically connect to the MCP server

## API Documentation

Once the server is running, you can access:

- Interactive API docs: `http://localhost:4891/docs`
- Alternative API docs: `http://localhost:4891/redoc`

## Usage Examples

### Basic Chat Completion

```bash
curl -X POST "http://localhost:4891/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama2",
    "messages": [
      {"role": "user", "content": "Hello, how are you?"}
    ]
  }'
```

### Streaming Chat Completion

```bash
curl -X POST "http://localhost:4891/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama2",
    "messages": [
      {"role": "user", "content": "Tell me a short story"}
    ],
    "stream": true
  }'
```

### With Parameters

```bash
curl -X POST "http://localhost:4891/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama2",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Explain quantum computing"}
    ],
    "temperature": 0.7,
    "max_tokens": 150
  }'
```

## Endpoints

- `GET /` - Root endpoint with basic information
- `GET /health` - Health check
- `POST /v1/chat/completions` - Chat completions (OpenAI-compatible)
- `GET /v1/models` - List available models

## Configuration

The following environment variables can be used:

- `OLLAMA_BASE_URL` - Base URL for Ollama API (default: `http://localhost:11434`)

## Requirements

- Python 3.8+
- uv package manager
- Ollama running locally
- Dependencies managed via pyproject.toml

## Notes

- The API converts between OpenAI and Ollama message formats automatically
- Token usage is estimated based on word count
- Make sure your Ollama models are pulled before using them
- The `/v1/models` endpoint returns a placeholder list - in production you might want to query Ollama directly for available models
