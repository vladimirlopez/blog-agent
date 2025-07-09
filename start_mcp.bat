@echo off
echo ================================================
echo          Starting Ollama Chat API (MCP)
echo ================================================
echo.
echo Checking prerequisites...
echo.

REM Check if uv is available
uv --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERROR: uv is not installed or not in PATH
    echo Please install uv first:
    echo    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    echo.
    pause
    exit /b 1
)

echo ✅ uv is available
echo.

REM Check if dependencies are installed
if not exist ".venv" (
    echo ⚠️  Virtual environment not found. Running uv sync...
    uv sync
    if %errorlevel% neq 0 (
        echo ❌ ERROR: Failed to install dependencies
        pause
        exit /b 1
    )
    echo ✅ Dependencies installed successfully
    echo.
)

echo ⚠️  IMPORTANT: Make sure Ollama is running at http://localhost:11434
echo    You can start Ollama with: ollama serve
echo.
echo Starting FastAPI server on port 4891 (MCP compatible)...
echo 📖 API Documentation: http://localhost:4891/docs
echo 🔗 API Endpoint: http://localhost:4891/v1/chat/completions
echo 🔧 MCP Server: Use 'uv run python mcp_server.py' in separate terminal
echo.
echo Press Ctrl+C to stop the server
echo.

set PORT=4891
uv run python main.py

echo.
echo Server stopped.
pause
