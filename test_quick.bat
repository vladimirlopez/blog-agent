@echo off
echo ================================================
echo        Quick Test - Ollama Chat API
echo ================================================
echo.

REM Check if server is running
echo Checking if API server is running...
curl -s http://localhost:4891/health >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ API server not running on port 4891
    echo.
    echo Please start the server first:
    echo    uv run python main.py
    echo    or
    echo    start_mcp.bat
    echo.
    pause
    exit /b 1
)

echo ✅ API server is running
echo.

REM Run the quick test script
echo Running comprehensive tests...
echo.
uv run python quick_test.py

echo.
echo Test completed. Check results above.
pause
