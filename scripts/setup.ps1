#!/usr/bin/env powershell
# Development setup script for Windows

Write-Host "🚀 Setting up Ollama Chat API development environment..." -ForegroundColor Green
Write-Host ""

# Check if uv is installed
try {
    $uvVersion = uv --version
    Write-Host "✅ uv is installed: $uvVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ uv is not installed. Installing..." -ForegroundColor Red
    Write-Host "Run: powershell -c `"irm https://astral.sh/uv/install.ps1 | iex`"" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "📦 Installing dependencies and creating virtual environment..." -ForegroundColor Blue
uv sync

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Dependencies installed successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "🎯 Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Make sure Ollama is running at http://localhost:11434" -ForegroundColor White
Write-Host "2. Run the server: uv run python main.py" -ForegroundColor White
Write-Host "3. Test the API: uv run python test_api.py" -ForegroundColor White
Write-Host "4. View docs at: http://localhost:8000/docs" -ForegroundColor White
