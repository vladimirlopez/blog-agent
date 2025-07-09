# VS Code MCP Integration - Quick Start Guide

## 🎉 Your MCP Integration is Ready!

Both the FastAPI server and MCP server are running and fully functional. Here's how to use them in VS Code:

## 📋 Current Status
- ✅ **FastAPI Server**: Running on port 4891
- ✅ **MCP Server**: Running and responding to requests
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
The blog-agent now supports interactive, collaborative writing where you work **with** the AI to create your blog post step by step.

#### **Step 1: Start a Writing Session**
```
# In VS Code, open your blog folder, then use Copilot Chat:
/start_writing_session topic="Your blog topic" blog_folder="."
```

#### **Step 2: Chat About Your Post**
```
# Have a conversation with the AI about your blog:
/chat_about_post session_id="session_20250709_143022" message="I want to write about FastAPI, but focus on the security aspects"

# Or ask for help:
/chat_about_post session_id="session_20250709_143022" message="Can you help me structure this post with an introduction, 3 main sections, and a conclusion?"
```

#### **Step 3: Iterative Development**
```
# Ask the AI to write specific sections:
/chat_about_post session_id="session_20250709_143022" message="Write an engaging introduction about why FastAPI security matters"

# Get feedback on your ideas:
/chat_about_post session_id="session_20250709_143022" message="I'm thinking of covering authentication, authorization, and HTTPS. What do you think?"
```

#### **Step 4: Update Your Draft**
```
# Update the draft with new content:
/update_draft session_id="session_20250709_143022" content="# FastAPI Security Guide\n\nSecurity is crucial..."

# Save when ready:
/save_draft session_id="session_20250709_143022"
```

#### **Step 5: Check Progress**
```
# Check your session status:
/get_session_status session_id="session_20250709_143022"
```

### **Benefits of Interactive Mode:**
- ✅ **Work in your blog folder** (not the agent folder)
- ✅ **Collaborative conversation** with the AI
- ✅ **Iterative development** - build your post step by step
- ✅ **Full control** over content and structure
- ✅ **Natural language** interaction
- ✅ **Conversational context** - AI remembers your discussion

## 🔧 Available MCP Tools

### **Original Tools:**
- **`chat_completion`**: Generate chat completions using Ollama models
- **`health_check`**: Check API health status
- **`list_models`**: List available Ollama models
- **`draft_post`**: Generate Quarto blog post drafts with content validation

### **Interactive Writing Tools:**
- **`start_writing_session`**: Start a new interactive writing session
- **`chat_about_post`**: Chat with AI about your blog post
- **`update_draft`**: Update the current blog post draft
- **`save_draft`**: Save the current draft to a file
- **`get_session_status`**: Get current writing session status

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
