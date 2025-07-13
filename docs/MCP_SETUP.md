# MCP (Model Context Protocol) Setup Guide

This guide explains how to set up the Ollama Chat API as an MCP server for VS Code integration.

## What is MCP?

Model Context Protocol (MCP) is a standard for connecting AI assistants to external tools and data sources. This allows VS Code to interact with your local Ollama models through a standardized protocol.

## Prerequisites

1. **VS Code with MCP Extension**: Install the MCP extension from the VS Code marketplace
2. **Ollama**: Running locally at `http://localhost:11434`
3. **UV**: Python package manager (installed via setup scripts)

## Setup Steps

### 1. Configure VS Code MCP Settings

The project includes a `.vscode/settings.json` file that configures MCP:

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

### 2. Start the FastAPI Server

The FastAPI server now runs on port 4891 (MCP compatible):

```bash
# Option 1: Use the MCP startup script
start_mcp.bat

# Option 2: Manual start
uv run python main.py
```

The server will be available at `http://localhost:4891`

### 3. Start the MCP Server

In a separate terminal, start the MCP server:

```bash
uv run python mcp_server.py
```

Or use the VS Code task: `Ctrl+Shift+P` → "Tasks: Run Task" → "start-mcp-server"

### 4. Test the Connection

You can test the MCP connection using VS Code's MCP tools panel or by using the API directly:

```bash
# Test the API endpoint
curl -X POST "http://localhost:4891/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama2",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

## Available MCP Tools

The MCP server provides these tools to VS Code:

### 1. `chat_completion`
- **Description**: Generate chat completions using Ollama models
- **Parameters**: 
  - `model`: Model name (e.g., "llama2", "codellama")
  - `messages`: Array of chat messages
  - `temperature`: Sampling temperature (0-2)
  - `max_tokens`: Maximum tokens to generate
  - `stream`: Whether to stream response

### 2. `health_check`
- **Description**: Check API health status
- **Parameters**: None

### 3. `list_models`
- **Description**: List available Ollama models
- **Parameters**: None

## Available Resources

The MCP server exposes these resources:

- **`/v1/chat/completions`**: Main chat endpoint
- **`/health`**: Health check endpoint
- **`/v1/models`**: Model listing endpoint

## Available Prompts

Pre-configured prompts for common use cases:

### 1. `system_prompt`
- **Description**: Default system prompt for chat completions
- **Arguments**: `role` (optional) - The role context for the assistant

### 2. `code_assistant`
- **Description**: System prompt for code-related tasks
- **Arguments**: `language` (optional) - Programming language context

## Troubleshooting

### MCP Server Not Starting

1. **Check dependencies**: Run `uv sync` to ensure all dependencies are installed
2. **Check Ollama**: Ensure Ollama is running at `http://localhost:11434`
3. **Check port**: Ensure port 4891 is available
4. **Check logs**: Look at the MCP server output for error messages

### VS Code Not Connecting

1. **Check MCP extension**: Ensure the MCP extension is installed and enabled
2. **Check settings**: Verify `.vscode/settings.json` is correctly configured
3. **Restart VS Code**: Sometimes a restart is needed after configuration changes
4. **Check workspace**: Ensure you're in the correct workspace folder

### API Errors

1. **Connection refused**: Check if FastAPI server is running on port 4891
2. **Ollama errors**: Ensure Ollama is running and has the requested model
3. **Timeout errors**: Increase timeout settings if needed

## Development

### Debugging MCP Server

Use the VS Code launch configuration "MCP Server" to debug the MCP server:

1. Set breakpoints in `mcp_server.py`
2. Press `F5` and select "MCP Server"
3. The debugger will attach to the MCP server process

### Adding New Tools

To add new MCP tools:

1. Add the tool definition to `_handle_list_tools()` in `mcp_server.py`
2. Add the tool implementation in `_handle_tool_call()`
3. Update the manifest file `mcp-manifest.json` if needed

### Testing MCP Protocol

You can test the MCP protocol directly using JSON-RPC:

```bash
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}' | uv run python mcp_server.py
```

## Configuration

### Environment Variables

- `OLLAMA_BASE_URL`: Base URL for Ollama API (default: `http://localhost:11434`)
- `MCP_SERVER_PORT`: Port for MCP server communication (default: `4891`)
- `PORT`: Port for FastAPI server (default: `4891`)

### Manifest File

The `mcp-manifest.json` file contains the complete MCP server configuration including:
- Server capabilities
- Tool definitions
- Resource definitions
- Prompt templates
- Configuration schema

## Integration Examples

### Using in VS Code

1. **Chat with Ollama**: Use the MCP chat completion tool in VS Code
2. **Code assistance**: Use the code assistant prompt for programming help
3. **Health monitoring**: Check API status using the health check tool

### Custom Integrations

The MCP server can be integrated with other MCP-compatible tools and applications beyond VS Code.

## Security Considerations

- The MCP server runs locally and connects to local Ollama instance
- No external network calls (except to local Ollama)
- Input validation through Pydantic models
- Proper error handling to prevent information leakage

---

For more information about Model Context Protocol, visit: https://modelcontextprotocol.io/
