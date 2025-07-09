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
uv run uvicorn main:app --reload --host 0.0.0.0 --port 4891
```

## Testing

```bash
# Run the basic test script
uv run python test_api.py

# Run comprehensive tests
uv run python quick_test.py

# Test draft post functionality
uv run python test_draft_post.py

# Install dev dependencies for testing
uv sync --group dev

# Run with pytest (if you add tests later)
uv run pytest
```

## Blog Post Generation

### Using the `/tool/draft_post` endpoint

The blog post generation feature allows you to create Quarto blog post drafts using Ollama models with enhanced content validation and statistics.

#### Web Interface

For the easiest experience, use the web interface:

1. **Start the server**: `uv run python main.py`
2. **Open your browser**: Navigate to `http://localhost:4891/static/index.html`
3. **Fill out the form**:
   - Enter your blog post topic
   - Select an AI model (Mistral 7B, Llama 2, or Code Llama)
   - Specify the blog folder (default: "posts")
4. **Generate**: Click "Generate Blog Post" and wait for the AI to create your draft

#### Direct API Usage

```bash
# Create a blog post draft via HTTP API
curl -X POST "http://localhost:4891/tool/draft_post" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Why I love teaching physics with AI",
    "model": "mistral:7b",
    "blog_folder": "posts"
  }'
```

**Enhanced Response Format:**
```json
{
  "filename": "2025-01-09-why-i-love-teaching-physics-with-ai.qmd",
  "preview": "# Why I Love Teaching Physics with AI\n\nArtificial Intelligence has revolutionized...",
  "full_path": "/path/to/blog-agent/posts/2025-01-09-why-i-love-teaching-physics-with-ai.qmd",
  "status": "success",
  "word_count": 1247,
  "content_stats": {
    "word_count": 1247,
    "heading_count": 5,
    "paragraph_count": 12,
    "code_blocks": 3,
    "links": 2,
    "images": 1,
    "character_count": 7834,
    "estimated_reading_time": 6
  },
  "content_issues": null
}
```

#### Enhanced Features

- **Content Validation**: Automatically checks word count, heading structure, and content quality
- **Statistics**: Provides detailed content statistics including reading time estimation
- **Model Validation**: Verifies that the requested AI model is available
- **Duplicate Prevention**: Automatically handles filename conflicts
- **Quality Warnings**: Alerts you to potential content issues

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
