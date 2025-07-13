# Blog Agent

A VS Code-integrated blog agent that uses local Ollama AI models to automate blog post creation through FastAPI and Model Context Protocol (MCP) servers.

## 🚀 Features

- **🤖 Local AI Integration**: Uses Ollama models running locally for privacy and control
- **🔧 VS Code Integration**: Direct integration through MCP for seamless workflow in your editor
- **💬 Interactive Writing**: Collaborative writing sessions with AI assistance
- **✅ Content Validation**: Automatic validation of generated content
- **📝 Quarto Support**: Generates properly formatted Quarto blog posts with YAML frontmatter
- **🔄 Multiple Workflows**: Both one-shot generation and iterative collaborative writing

## 📁 Project Structure

```
blog-agent/
├── src/                    # Source code
│   ├── main.py            # FastAPI server
│   ├── mcp_server.py      # MCP server implementation
│   ├── interactive_agent.py # Interactive writing agent
│   ├── content_validator.py # Content validation
│   ├── ollama_client.py   # Ollama API client
│   └── schemas.py         # Data schemas
├── tests/                 # Test files
│   ├── test_api.py        # API tests
│   ├── test_draft_post.py # Blog generation tests
│   └── quick_test.py      # Quick functionality tests
├── scripts/               # Setup and utility scripts
│   ├── setup.ps1          # PowerShell setup
│   ├── setup.sh           # Bash setup
│   └── start_mcp.bat      # MCP server launcher
├── docs/                  # Documentation
│   ├── README.md          # Documentation index
│   ├── VSCODE_MCP_GUIDE.md # Main usage guide
│   ├── MCP_SETUP.md       # MCP setup instructions
│   └── DEVELOPMENT.md     # Development guide
├── config/                # Configuration files
│   └── mcp-manifest.json  # MCP manifest
├── posts/                 # Generated blog posts
├── static/                # Static assets
└── .vscode/              # VS Code configuration
```

## ⚡ Quick Start

### 1. Prerequisites
- Python 3.8+
- [Ollama](https://ollama.ai/) installed and running
- VS Code with GitHub Copilot

### 2. Installation
```bash
# Clone the repository
git clone <repository-url>
cd blog-agent

# Install dependencies
uv sync
```

### 3. Setup
```bash
# Run the setup script (Windows)
.\scripts\setup.ps1

# Or manually start Ollama (if not already running)
ollama serve

# Pull required models
ollama pull mistral:7b
```

### 4. Start the Servers
```bash
# Start MCP server
.\scripts\start_mcp.bat

# Or manually
uv run python -m src.mcp_server
```

### 5. Use in VS Code
1. Open VS Code in your blog project folder
2. Open Copilot Chat (`Ctrl+Shift+I`)
3. Use commands:
   - `/draft_post topic="Your blog topic"` - Generate complete blog post
   - `/start_writing_session topic="Your topic" blog_folder="."` - Start interactive session
   - `/chat message="..."` - Chat about your active post (simplified!)
   - `/update content="..."` - Update your active post
   - `/save` - Save your active post

## 🎯 Usage Modes

### One-Shot Blog Generation
Perfect for quick blog post creation:
```
/draft_post topic="Getting Started with FastAPI"
```

### Interactive Collaborative Writing
Ideal for iterative, conversational blog development:

```
# Start session
/start_writing_session topic="Docker for Beginners" blog_folder="."

# Chat and develop ideas (no session ID needed!)
/chat message="Help me structure this post"

# Update draft with new content
/update content="# Your content here"

# Save when done
/save
```

## 🧪 Testing

```bash
# Run all tests
cd tests
python test_api.py
python test_draft_post.py

# Quick functionality test
python quick_test.py
```

## 📚 Documentation

- **[Documentation Index](docs/README.md)** - Overview of all documentation
- **[VS Code MCP Guide](docs/VSCODE_MCP_GUIDE.md)** - Complete setup and usage instructions
- **[MCP Setup](docs/MCP_SETUP.md)** - Model Context Protocol configuration
- **[Development Guide](docs/DEVELOPMENT.md)** - Development and contribution guidelines
- **[Interactive Writing Guide](docs/INTERACTIVE_WRITING_GUIDE.md)** - Detailed interactive workflow examples

## 🔧 Configuration

The project uses:
- **FastAPI Server**: Port 4891 (configurable)
- **Ollama API**: Port 11434 (default)
- **MCP Integration**: Through VS Code extensions

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 📄 License

[Add your license information here]

## 🆘 Troubleshooting

**Common Issues:**
- **Ollama not running**: Ensure `ollama serve` is running
- **Port conflicts**: Check if ports 4891 or 11434 are available
- **VS Code integration**: Restart VS Code after configuration changes

For detailed troubleshooting, see the [VS Code MCP Guide](docs/VSCODE_MCP_GUIDE.md).
