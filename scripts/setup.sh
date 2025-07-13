#!/bin/bash
# Development setup script for Unix-like systems

echo "🚀 Setting up Ollama Chat API development environment..."
echo ""

# Check if uv is installed
if command -v uv &> /dev/null; then
    echo "✅ uv is installed: $(uv --version)"
else
    echo "❌ uv is not installed. Installing..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi

echo ""
echo "📦 Installing dependencies and creating virtual environment..."
uv sync

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully!"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "🎯 Setup complete!"
echo ""
echo "Next steps:"
echo "1. Make sure Ollama is running at http://localhost:11434"
echo "2. Run the server: uv run python main.py"
echo "3. Test the API: uv run python test_api.py"
echo "4. View docs at: http://localhost:8000/docs"
