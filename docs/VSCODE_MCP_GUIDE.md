# VS Code MCP Integration - Quick Start Guide

## 🎉 Your MCP Integration is Ready!

Both the FastAPI server and MCP server are running and fully functional. Here's how to use them in VS Code:

## 📋 Current Status
- ✅ **FastAPI Server**: Running on port 4891
- ✅ **MCP Server**: Running and responding to requests
- ✅ **Ollama**: Running on port 11434 with models available
- ✅ **MCP Extensions**: Installed (Copilot MCP, MCP Server Runner)
- ✅ **VS Code Configuration**: Properly configured

## 🚀 How to Use MCP in VS Code

### 1. **Using VS Code Tasks**
Press `Ctrl+Shift+P` → Type "Tasks: Run Task" → Select:
- **`start-mcp-full`**: Start both FastAPI and MCP servers
- **`test-mcp-connection`**: Test MCP server connectivity

### 2. **Using MCP Server Runner Extension**
- Open the MCP Server Runner panel from the sidebar
- Your "ollama-chat-api" server should appear
- Manage server status and view logs

### 3. **Using GitHub Copilot Chat with MCP**
- Open Copilot Chat panel (`Ctrl+Shift+I`)
- The MCP server provides context about your local models
- Ask questions like:
  - "What models are available?"
  - "Generate a response using mistral:7b"
  - "Check the health of the API"
  - "Generate a blog post about FastAPI"
- Or use the direct commands:
  - `/draft_post topic="Your blog topic here"`
  - `/chat_completion model="mistral:7b" message="Hello world"`

### 4. **Direct MCP Commands**
Press `Ctrl+Shift+P` → Type "MCP" to see available commands:
- **MCP: Execute Tool**
- **MCP: List Tools**
- **MCP: Server Status**

## 🎯 Interactive Blog Writing Workflow

### **New: Collaborative Writing Mode**
The blog-agent now supports interactive, collaborative writing where you work **with** the AI to create your blog post step by step. This mode allows you to work directly in your blog folder and have natural conversations with the AI about your content.

#### **Step 1: Start a Writing Session**
**What it does:** Creates a new writing session with the AI, initializing a conversation context and creating a draft file in your current folder.

**How to use:**
1. Open VS Code in your blog folder (not the blog-agent folder)
2. Open Copilot Chat (`Ctrl+Shift+I`)
3. Type: `/start_writing_session topic="Your blog topic" blog_folder="."`

**Example:**
```
/start_writing_session topic="FastAPI Security Best Practices" blog_folder="."
```

**What happens:**
- Creates a session ID (e.g., `session_20250709_143022`)
- Initializes an empty draft file
- Sets up conversation context about your topic
- Returns session details for reference

#### **Step 2: Chat About Your Post**
**What it does:** Engage in natural conversation with the AI about your blog post. The AI remembers the context and helps you develop ideas.

**How to use:**
```
/chat_about_post session_id="your_session_id" message="Your natural language message"
```

**Examples:**
```
# Discuss focus and scope
/chat_about_post session_id="session_20250709_143022" message="I want to write about FastAPI, but focus specifically on the security aspects that developers often overlook"

# Ask for structure help
/chat_about_post session_id="session_20250709_143022" message="Can you help me structure this post with an engaging introduction, 3 main sections, and a practical conclusion?"

# Get content suggestions
/chat_about_post session_id="session_20250709_143022" message="What are the most important security vulnerabilities in FastAPI that I should cover?"

# Ask for writing help
/chat_about_post session_id="session_20250709_143022" message="Write an engaging introduction that explains why FastAPI security matters to developers"
```

**What happens:**
- AI responds with suggestions, content, or questions
- Conversation history is maintained
- Context builds up over the session

#### **Step 3: Update Your Draft**
**What it does:** Updates your draft file with new content while preserving the conversation history.

**How to use:**
```
/update_draft session_id="your_session_id" content="Your markdown content here"
```

**Example:**
```
/update_draft session_id="session_20250709_143022" content="# FastAPI Security Best Practices

## Introduction

FastAPI has become one of the most popular Python web frameworks due to its speed, ease of use, and automatic API documentation. However, with great power comes great responsibility, especially when it comes to security..."
```

**What happens:**
- Overwrites the current draft with new content
- Maintains proper Quarto/Markdown formatting
- Preserves the session for continued conversation

#### **Step 4: Save Your Draft**
**What it does:** Saves the current draft to a permanent file with proper naming and formatting.

**How to use:**
```
/save_draft session_id="your_session_id"
```

**What happens:**
- Creates a file named `YYYY-MM-DD-topic-slug.qmd`
- Adds proper YAML frontmatter
- Saves to your current directory
- Provides file path confirmation

#### **Step 5: Check Progress**
**What it does:** Shows you the current status of your writing session including conversation history and draft content.

**How to use:**
```
/get_session_status session_id="your_session_id"
```

**What you get:**
- Session information (topic, start time, etc.)
- Conversation history summary
- Current draft preview
- File status and location

### **Complete Example Workflow:**

```bash
# 1. Start session
/start_writing_session topic="Getting Started with Docker" blog_folder="."

# 2. Discuss structure
/chat_about_post session_id="session_20250709_143022" message="I want to write a beginner-friendly guide to Docker. What should I cover?"

# 3. Get specific content
/chat_about_post session_id="session_20250709_143022" message="Write me an introduction that explains what Docker is and why beginners should care about it"

# 4. Update draft with the introduction
/update_draft session_id="session_20250709_143022" content="# Getting Started with Docker

## What is Docker and Why Should You Care?

Docker has revolutionized how we develop, deploy, and manage applications..."

# 5. Continue the conversation
/chat_about_post session_id="session_20250709_143022" message="Now help me write a section about installing Docker on different operating systems"

# 6. Save when finished
/save_draft session_id="session_20250709_143022"
```

### **Key Benefits of Interactive Mode:**
- ✅ **Work in your blog folder** - Files are created directly where you need them
- ✅ **Collaborative conversation** - Natural language interaction with the AI
- ✅ **Iterative development** - Build your post step by step, section by section
- ✅ **Full control** - You decide what content to keep, modify, or discard
- ✅ **Conversational context** - AI remembers your discussion and maintains context
- ✅ **Flexible workflow** - Write, discuss, revise, and improve naturally
- ✅ **Proper formatting** - Automatic Quarto/Markdown formatting and frontmatter

## 🔧 Available MCP Tools

### **One-Shot Blog Generation**
- **`chat_completion`**: Generate chat completions using Ollama models
- **`health_check`**: Check API health status
- **`list_models`**: List available Ollama models
- **`draft_post`**: Generate complete Quarto blog post drafts with content validation

### **Interactive Writing Tools**
- **`start_writing_session`**: Begin a collaborative writing session with conversation context
  - Creates session ID, initializes draft file in your current folder
  - Sets up conversation context for iterative writing
- **`chat_about_post`**: Have natural language conversations about your blog post
  - Maintains conversation history and context
  - Provides suggestions, content, and writing assistance
- **`update_draft`**: Update your draft file with new content while maintaining context
  - Overwrites current draft with new content
  - Preserves proper Quarto/Markdown formatting
- **`save_draft`**: Save the current draft to a permanent file with proper formatting
  - Creates properly named file with YAML frontmatter
  - Saves to your current directory
- **`get_session_status`**: Check the status of your writing session and conversation history
  - Shows session information and conversation summary
  - Displays current draft preview

## 🧪 Test Commands
```bash
# Test MCP server directly
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}' | uv run python mcp_server.py

# Test health check
echo '{"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": "health_check", "arguments": {}}}' | uv run python mcp_server.py

# Test chat completion
echo '{"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "chat_completion", "arguments": {"model": "mistral:7b", "messages": [{"role": "user", "content": "Hello!"}]}}}' | uv run python mcp_server.py

# Test draft_post tool
echo '{"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "draft_post", "arguments": {"topic": "Getting Started with AI"}}}' | uv run python mcp_server.py
```

## 🔄 Restart Instructions
If you need to restart VS Code to pick up the new configuration:
1. Close VS Code
2. Make sure both servers are running:
   - FastAPI: `.\start_mcp.bat`
   - MCP: `uv run python mcp_server.py`
3. Reopen VS Code
4. The MCP integration should be automatically available

## 🎯 Next Steps
1. **Try the MCP tools** in VS Code
2. **Use Copilot Chat** with your local models
3. **Build custom workflows** using the MCP integration
4. **Explore the MCP Server Runner** extension features

**Your VS Code is now fully integrated with your local Ollama models through MCP!** 🚀
