# Development Commands

This document contains common development commands for the Ollama Chat API project using uv.

## Initial Setup

```bash
# Install uv (if not already installed)
# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```bash
# Setup project (automated)
# Windows
.\setup.ps1

# macOS/Linux
chmod +x setup.sh && ./setup.sh

# Or manually
uv sync
```

## Running the Application

```bash
# Run the main application
uv run python main.py

# Or with uvicorn directly
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Testing

```bash
# Run the test script
uv run python test_api.py

# Install dev dependencies for testing
uv sync --group dev

# Run with pytest (if you add tests later)
uv run pytest
```

## Development Tools

```bash
# Format code with black
uv run black .

# Lint with flake8
uv run flake8 .

# Type checking with mypy
uv run mypy .

# Install all dev dependencies
uv sync --group dev
```

## Dependency Management

```bash
# Add a new dependency
uv add package-name

# Add a dev dependency
uv add --group dev package-name

# Remove a dependency
uv remove package-name

# Update dependencies
uv sync --upgrade

# Show installed packages
uv pip list
```

## Environment Management

```bash
# Activate virtual environment
# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

# Run commands in the virtual environment
uv run python script.py

# Show Python interpreter path
uv run python -c "import sys; print(sys.executable)"
```

## Useful Commands

```bash
# Show project info
uv info

# Show dependency tree
uv tree

# Create requirements.txt (if needed for deployment)
uv pip freeze > requirements.txt

# Build the project
uv build

# Publish to PyPI (if configured)
uv publish
```
