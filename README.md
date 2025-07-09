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

## MCP (Model Context Protocol) Integration - SETUP COMPLETE! ✅

This project includes **full MCP support** for VS Code integration. The setup is **already configured** and ready to use!

### ✅ What's Already Done:
- **MCP Extensions**: Installed `Copilot MCP` and `MCP Server Runner`
- **VS Code Configuration**: `.vscode/settings.json` properly configured
- **MCP Server**: `mcp_server.py` implemented with JSON-RPC 2.0 support
- **MCP Manifest**: `mcp-manifest.json` defines all capabilities

### 🚀 **Quick Start - VS Code Integration:**

1. **Start the FastAPI server** (if not already running):
   ```bash
   .\start_mcp.bat
   ```

2. **Start the MCP server** (in a separate terminal):
   ```bash
   uv run python mcp_server.py
   ```

3. **Restart VS Code** to pick up the new extensions and configuration

4. **Access MCP Tools in VS Code**:
   - Open the Command Palette (`Ctrl+Shift+P`)
   - Type "MCP" to see available MCP commands
   - Use the MCP Server Runner extension to manage your server
   - Use GitHub Copilot Chat with MCP integration

### 🔧 **Available MCP Tools:**
- **`chat_completion`**: Generate chat completions using your Ollama models
- **`health_check`**: Check API health status  
- **`list_models`**: List available Ollama models

### 💡 **How to Use in VS Code:**

1. **With GitHub Copilot Chat**:
   - Open Copilot Chat panel
   - The MCP server will automatically provide context about your local models
   - You can directly use your local Ollama models through the chat interface

2. **With MCP Server Runner**:
   - Open the MCP Server Runner extension panel
   - Your "ollama-chat-api" server should appear as configured
   - Manage server status and view logs

3. **Direct MCP Commands**:
   - Use Command Palette → "MCP: Execute Tool"
   - Select from available tools (chat_completion, health_check, list_models)

### 🎯 **Test Your Integration:**
```bash
# Test MCP server directly
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}' | uv run python mcp_server.py
```

**Expected Output**: JSON response listing available tools

### 📋 **Current Configuration:**
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

### 🔍 **Troubleshooting:**
- **MCP not working?** → Restart VS Code after installing extensions
- **Server not connecting?** → Check that both FastAPI and MCP servers are running
- **No tools available?** → Verify MCP server responds to `tools/list` command
- **Models not found?** → Ensure Ollama is running and models are pulled

**📚 For detailed setup instructions, see [MCP_SETUP.md](MCP_SETUP.md)**

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
    "model": "mistral:7b",
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
    "model": "mistral:7b",
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
    "model": "mistral:7b",
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
