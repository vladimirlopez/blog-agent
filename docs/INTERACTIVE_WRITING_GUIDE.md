# Interactive Blog Writing Guide

## 🎯 Overview

The blog-agent now supports interactive, collaborative writing where you work **with** the AI to create your blog post step by step. This mode gives you full control over the writing process and allows natural language conversations about your content.

## 🚀 Quick Start

### 1. **Setup**
```bash
# Navigate to your blog folder (not the blog-agent folder)
cd "c:\path\to\your\blog"

# Open VS Code in your blog folder
code .

# Make sure blog-agent is running (in a separate terminal)
cd "c:\Users\vladi\AI Projects\blog-agent"
.\start_mcp.bat
```

### 2. **Start Writing Session**
```bash
# In VS Code Copilot Chat (Ctrl+Shift+I)
/start_writing_session topic="Your Blog Topic" blog_folder="."
```

### 3. **Collaborate with AI**
```bash
# Have natural conversations about your post (no session ID needed!)
/chat message="Help me structure this post"
```

### 4. **Build Your Post**
```bash
# Update your draft with new content
/update content="# Your content here"
```

### 5. **Save When Ready**
```bash
# Save the final post
/save
```

## 📋 Available Interactive Tools

### `start_writing_session`
**Purpose:** Begin a new interactive writing session

**Parameters:**
- `topic` (required): The topic for your blog post
- `blog_folder` (optional): Target folder for the draft (default: ".")

**Example:**
```bash
/start_writing_session topic="Docker for Python Developers" blog_folder="."
```

**Returns:**
- Session ID (e.g., `session_20250709_143022`)
- Temporary draft file path
- Session initialization confirmation

### `chat` (Simplified Command)
**Purpose:** Have natural language conversations about your active blog post (no session ID needed!)

**Parameters:**
- `message` (required): Your message to the AI

**Examples:**
```bash
# Get structure suggestions
/chat message="How should I structure this post about Docker?"

# Request specific content
/chat message="Write an engaging introduction about Docker for Python developers"

# Ask for improvements
/chat message="Can you make this section more beginner-friendly?"

# Get code examples
/chat message="I need a practical Docker example for a Python web app"
```

**Legacy Command:** You can still use `/chat_about_post session_id="..." message="..."` if needed

**Returns:**
- AI response with suggestions, content, or questions
- Updated conversation context
- Content recommendations

### `update` (Simplified Command)
**Purpose:** Update your active draft file with new content (no session ID needed!)

**Parameters:**
- `content` (required): The new content for your draft (Markdown format)

**Example:**
```bash
/update content="# Docker for Python Developers

## Introduction

Docker has revolutionized how we develop, ship, and run applications. For Python developers, Docker solves many common problems like dependency management, environment consistency, and deployment complexity.

## Why Docker Matters for Python Development

Python projects often suffer from the \"it works on my machine\" problem..."
```

**Legacy Command:** You can still use `/update_draft session_id="..." content="..."` if needed

**Returns:**
- Confirmation of draft update
- Current draft preview
- File location information

### `save` (Simplified Command)
**Purpose:** Save your current active draft to a permanent file with proper formatting (no session ID needed!)

**Parameters:**
- None required! Works with your active session

**Example:**
```bash
/save
```

**Legacy Command:** You can still use `/save_draft session_id="..."` if needed

**Returns:**
- Final filename (e.g., `2025-07-09-docker-for-python-developers.qmd`)
- Full file path
- Confirmation of save operation

### `status` (Simplified Command)
**Purpose:** Check the status of your active writing session (no session ID needed!)

**Parameters:**
- None required! Works with your active session

**Example:**
```bash
/status
```

**Legacy Command:** You can still use `/get_session_status session_id="..."` if needed

**Returns:**
- Session information (topic, start time, file location)
- Conversation history summary
- Current draft preview
- Word count and progress metrics

## 🎨 Complete Example Workflow

Here's a real-world example of using the interactive writing tools:

### Step 1: Start Session
```bash
# Navigate to your blog folder
cd "c:\Users\yourname\myblog"
code .

# Start writing session
/start_writing_session topic="Getting Started with TypeScript" blog_folder="."
```

**Response:**
```
✅ Writing session started!
📝 Session ID: session_20250709_143022
📁 Draft file: ./draft_session_20250709_143022.md
🎯 Topic: Getting Started with TypeScript
```

### Step 2: Plan Structure
```bash
/chat message="I want to write about TypeScript for JavaScript developers. What would be a good structure for this post?"
```

**AI Response:**
```
Great topic! Here's a suggested structure for your TypeScript post:

1. **Introduction** - What is TypeScript and why it matters
2. **Why TypeScript?** - Benefits over vanilla JavaScript
3. **Installation & Setup** - Getting started quickly
4. **Basic Types** - String, number, boolean, arrays, objects
5. **Interfaces & Type Definitions** - Creating custom types
6. **Functions with Types** - Typed parameters and return values
7. **Real-world Example** - Building a small project
8. **Conclusion** - Next steps and resources

Would you like me to help you write any specific section?
```

### Step 3: Write Introduction
```bash
/chat message="Write an engaging introduction that explains what TypeScript is and why JavaScript developers should care about it"
```

**AI Response:**
```
Here's an engaging introduction for your TypeScript post:

If you've been writing JavaScript for a while, you've probably encountered those frustrating bugs that could have been caught at compile time—undefined property access, function calls with wrong parameters, or subtle type mismatches that only surface in production. TypeScript is Microsoft's answer to these problems, offering static type checking while maintaining the flexibility and expressiveness that makes JavaScript great.

TypeScript isn't just "JavaScript with types"—it's a powerful development tool that can catch errors before they reach your users, improve code documentation, and make large codebases more maintainable. The best part? You can adopt it gradually in existing projects without rewriting everything.

Would you like me to continue with the next section?
```

### Step 4: Update Draft
```bash
/update content="# Getting Started with TypeScript

## Introduction

If you've been writing JavaScript for a while, you've probably encountered those frustrating bugs that could have been caught at compile time—undefined property access, function calls with wrong parameters, or subtle type mismatches that only surface in production. TypeScript is Microsoft's answer to these problems, offering static type checking while maintaining the flexibility and expressiveness that makes JavaScript great.

TypeScript isn't just \"JavaScript with types\"—it's a powerful development tool that can catch errors before they reach your users, improve code documentation, and make large codebases more maintainable. The best part? You can adopt it gradually in existing projects without rewriting everything."
```

### Step 5: Continue Building
```bash
/chat message="Now I need a section about installation and setup. Make it practical with step-by-step instructions"
```

### Step 6: Check Progress
```bash
/status
```

**Response:**
```
📊 Session Status Report

🎯 Topic: Getting Started with TypeScript
⏰ Started: 2025-07-09 14:30:22
📁 Draft File: ./draft_session_20250709_143022.md
💬 Conversation Messages: 4
📝 Current Word Count: 287 words

Recent Activity:
- Introduction written and updated
- Structure discussion completed
- Installation section requested

Current Draft Preview:
# Getting Started with TypeScript

## Introduction

If you've been writing JavaScript for a while, you've probably encountered those frustrating bugs that could have been caught at compile time...
```

### Step 7: Finalize and Save
```bash
/save
```

**Response:**
```
✅ Draft saved successfully!
📄 Filename: 2025-07-09-getting-started-with-typescript.qmd
📁 Location: c:\Users\yourname\myblog\2025-07-09-getting-started-with-typescript.qmd
📊 Final stats: 1,456 words, 7 headings, ~7 min read
```

## 💡 Pro Tips

### Effective Conversation Strategies

1. **Be Specific**
   - ❌ "Write about TypeScript"
   - ✅ "Write an introduction explaining what TypeScript is and why JavaScript developers should care about it"

2. **Ask for Structure First**
   ```bash
   /chat message="Help me plan the structure of this post about React hooks"
   ```

3. **Request Specific Content Types**
   ```bash
   # For code examples
   /chat message="I need a practical code example showing how to use useState"
   
   # For explanations
   /chat message="Explain the difference between let and const in simple terms"
   
   # For improvements
   /chat message="Can you make this section more engaging and add some humor?"
   ```

4. **Use the AI for Review**
   ```bash
   /chat message="I've written a section about closures. Can you review it and suggest improvements?"
   ```

### Building Content Iteratively

1. **Start with Structure**
   - Plan your outline first
   - Get AI suggestions for section organization
   - Build section by section

2. **Write in Chunks**
   - Write one section at a time
   - Update draft frequently
   - Review and refine as you go

3. **Use Conversation History**
   - The AI remembers your previous discussions
   - Reference earlier conversations
   - Build on established context

### Session Management

1. **Check Status Regularly**
   ```bash
   /get_session_status session_id="your_id"
   ```

2. **Save Multiple Versions**
   - You can save drafts multiple times
   - Each save creates a new file with timestamp
   - Useful for creating different versions

3. **Plan Your Sessions**
   - One session per blog post
   - Use descriptive topics
   - Work in focused chunks

## 🔄 Workflow Patterns

### Pattern 1: Collaborative Planning
```bash
# 1. Start session
/start_writing_session topic="React Performance Optimization"

# 2. Plan structure
/chat_about_post message="Help me structure this post about React performance"

# 3. Refine focus
/chat_about_post message="I want to focus on practical tips, not theory. What should I cover?"

# 4. Get section suggestions
/chat_about_post message="What are the most impactful performance optimizations?"
```

### Pattern 2: Section-by-Section Building
```bash
# 1. Write introduction
/chat_about_post message="Write an introduction about React performance"

# 2. Update draft
/update_draft content="# React Performance Optimization\n\n## Introduction\n\n[content]"

# 3. Write next section
/chat_about_post message="Now write a section about memo and useMemo"

# 4. Continue iteratively...
```

### Pattern 3: Review and Refine
```bash
# 1. Get AI feedback
/chat_about_post message="Review my introduction and suggest improvements"

# 2. Ask for specific changes
/chat_about_post message="Make this section more beginner-friendly"

# 3. Request additions
/chat_about_post message="Add a practical code example here"
```

## 🚫 Common Pitfalls

### Don't Do This:
- Start sessions without planning
- Write huge sections all at once
- Ignore conversation context
- Forget to save your work
- Try to write everything in one message

### Do This Instead:
- Plan your structure first
- Build incrementally
- Use conversation history
- Save drafts regularly
- Have focused conversations

## 🎯 When to Use Interactive vs One-Shot

### Use Interactive Writing When:
- You want to collaborate with the AI
- You need to iterate and refine content
- You're working on complex topics
- You want full control over the process
- You're writing in your blog folder

### Use One-Shot Generation When:
- You need a quick, complete post
- You want to generate multiple posts
- You're comfortable with AI's first attempt
- You prefer minimal interaction

## 🔧 Technical Details

### Session Storage
- Sessions are stored temporarily in memory
- Draft files are created in your current folder
- Conversation history is maintained per session
- Sessions expire after 24 hours of inactivity

### File Naming
- Draft files: `draft_session_YYYYMMDD_HHMMSS.md`
- Final files: `YYYY-MM-DD-topic-slug.qmd`
- Automatic duplicate prevention
- Proper YAML frontmatter added

### Content Formatting
- Markdown formatting preserved
- Code blocks properly formatted
- YAML frontmatter automatically added
- Quarto-compatible output

## 🆘 Troubleshooting

### Session Not Found
```bash
# Check if session exists
/get_session_status session_id="your_session_id"

# If not found, start a new session
/start_writing_session topic="Your Topic"
```

### AI Not Responding
- Check that blog-agent MCP server is running
- Verify VS Code MCP integration is active
- Restart VS Code if needed

### Draft Not Updating
- Verify session ID is correct
- Check file permissions in your blog folder
- Ensure content is valid Markdown

### Can't Save Draft
- Check write permissions in target folder
- Verify session has content to save
- Try updating draft first, then saving

## 📚 Additional Resources

- [Main Documentation](./DEVELOPMENT.md)
- [VS Code MCP Guide](./VSCODE_MCP_GUIDE.md)
- [End-to-End Guide](./END_TO_END_GUIDE.md)
- [MCP Server Documentation](./MCP_SETUP.md)

---

**Happy Interactive Writing!** 🎉
