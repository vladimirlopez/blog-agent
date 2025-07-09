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

## Interactive Blog Writing (New Feature)

### Using the Interactive Writing Tools

The blog-agent now supports interactive, collaborative writing where you work **with** the AI to create your blog post step by step. This is different from the one-shot generation and gives you full control over the writing process.

#### **How Interactive Writing Works**

1. **Work in your blog folder** - Navigate to your actual blog repository
2. **Start a writing session** - Initialize a conversation with the AI
3. **Collaborate iteratively** - Have natural language conversations about your content
4. **Update your draft** - Build your post section by section
5. **Save when ready** - Export to a properly formatted blog post file

#### **Step-by-Step Interactive Workflow**

**Step 1: Navigate to Your Blog Folder**
```bash
# Change to your blog directory (not the blog-agent folder)
cd "c:\path\to\your\blog"

# Open VS Code in your blog folder
code .
```

**Step 2: Start a Writing Session**
```bash
# In VS Code Copilot Chat (Ctrl+Shift+I)
/start_writing_session topic="Your Blog Topic Here" blog_folder="."

# Example:
/start_writing_session topic="Building REST APIs with FastAPI" blog_folder="."
```

**What happens:**
- Creates a unique session ID (e.g., `session_20250709_143022`)
- Initializes a temporary draft file in your current folder
- Sets up conversation context about your topic
- Returns session details for reference

**Step 3: Have Natural Conversations**
```bash
# Discuss your post structure
/chat_about_post session_id="session_20250709_143022" message="I want to write about FastAPI, but I'm not sure how to structure it. Can you help me plan the sections?"

# Get content suggestions
/chat_about_post session_id="session_20250709_143022" message="What are the most important FastAPI concepts that beginners should understand?"

# Ask for specific content
/chat_about_post session_id="session_20250709_143022" message="Write me an engaging introduction that explains what FastAPI is and why developers should care about it"

# Get writing feedback
/chat_about_post session_id="session_20250709_143022" message="I've written a section about routing. Can you review it and suggest improvements?"
```

**Step 4: Update Your Draft**
```bash
# Update the draft with new content
/update_draft session_id="session_20250709_143022" content="# Building REST APIs with FastAPI

## Introduction

FastAPI is a modern, fast web framework for building APIs with Python 3.7+ based on standard Python type hints. It's designed to be easy to use and learn, while providing high performance and automatic API documentation.

## Why Choose FastAPI?

FastAPI offers several advantages over traditional Python web frameworks..."
```

**Step 5: Continue the Conversation**
```bash
# Ask for the next section
/chat_about_post session_id="session_20250709_143022" message="Now I need a section about setting up a basic FastAPI project. Can you write that for me?"

# Get code examples
/chat_about_post session_id="session_20250709_143022" message="I need a practical code example showing how to create a simple API endpoint with FastAPI"

# Ask for improvements
/chat_about_post session_id="session_20250709_143022" message="Can you make this section more engaging and add some practical tips?"
```

**Step 6: Check Your Progress**
```bash
# Check session status
/get_session_status session_id="session_20250709_143022"
```

**What you get:**
- Session information (topic, start time, file location)
- Conversation history summary
- Current draft preview
- Word count and progress metrics

**Step 7: Save Your Final Post**
```bash
# Save the final draft
/save_draft session_id="session_20250709_143022"
```

**What happens:**
- Creates a file named `2025-07-09-building-rest-apis-with-fastapi.qmd`
- Adds proper YAML frontmatter with title, description, date, categories
- Saves to your current directory (your blog folder)
- Provides confirmation with file path

#### **Real-World Example Workflow**

Here's a complete example of how you might use the interactive writing tools:

```bash
# 1. Start in your blog folder
cd "c:\Users\yourname\myblog"
code .

# 2. Start writing session
/start_writing_session topic="Docker for Python Developers" blog_folder="."
# Returns: session_20250709_143022

# 3. Plan the structure
/chat_about_post session_id="session_20250709_143022" message="I want to write about Docker for Python developers. What would be a good structure for this post?"
# AI suggests: Introduction, Why Docker, Installation, Basic Commands, Python-specific examples, etc.

# 4. Get introduction
/chat_about_post session_id="session_20250709_143022" message="Write an engaging introduction that explains what Docker is and why Python developers should care about it"
# AI provides introduction content

# 5. Update draft with introduction
/update_draft session_id="session_20250709_143022" content="# Docker for Python Developers

## Introduction

Docker has revolutionized how we develop, ship, and run applications. For Python developers, Docker solves many common problems like dependency management, environment consistency, and deployment complexity..."

# 6. Get next section
/chat_about_post session_id="session_20250709_143022" message="Now I need a section about installing Docker. Make it practical with step-by-step instructions"

# 7. Continue building the post iteratively...
# 8. Save when finished
/save_draft session_id="session_20250709_143022"
```

#### **Key Benefits of Interactive Writing**

- **Natural Conversation**: Talk to the AI like you would a writing partner
- **Iterative Development**: Build your post section by section, paragraph by paragraph
- **Full Control**: You decide what content to keep, modify, or discard
- **Contextual Memory**: The AI remembers your conversation and maintains context
- **Work in Your Blog Folder**: Files are created directly where you need them
- **Flexible Workflow**: Write, discuss, revise, and improve at your own pace
- **Professional Output**: Automatic formatting and proper blog post structure

#### **Tips for Effective Interactive Writing**

1. **Be Specific**: Instead of "write about FastAPI," say "write an introduction explaining what FastAPI is and why it's better than Flask for API development"

2. **Ask for Structure**: Start by asking the AI to help you plan the overall structure of your post

3. **Iterate Gradually**: Build your post section by section rather than trying to write everything at once

4. **Use Natural Language**: Talk to the AI naturally - "Can you make this more engaging?" or "I need a code example here"

5. **Review and Refine**: Use the AI to review your own content and suggest improvements

6. **Check Progress**: Use `/get_session_status` to see your conversation history and current draft

7. **Save Regularly**: You can save drafts multiple times as you progress

#### **Interactive vs One-Shot Generation**

**Use Interactive Writing When:**
- You want to collaborate with the AI
- You need to iterate and refine content
- You want full control over the writing process
- You're working on complex or technical topics
- You want to work directly in your blog folder

**Use One-Shot Generation When:**
- You need a quick, complete blog post
- You want to generate multiple posts rapidly
- You're comfortable with the AI's first attempt
- You prefer minimal interaction
