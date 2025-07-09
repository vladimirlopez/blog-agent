# Blog Agent - Complete End-to-End Usage Guide

## 🚀 From Computer Startup to Published Post

This guide walks you through the complete process of using the blog-agent from turning on your computer to checking that your blog post is online.

## 📋 Prerequisites

Before starting, ensure you have:
- Windows 10/11 computer
- VS Code installed with MCP extensions
- Ollama installed and running
- Git configured for your repository
- Blog repository set up (e.g., GitHub Pages, Quarto blog)

## 🎯 Step-by-Step Process

### **Phase 1: System Setup & Startup**

#### 1. **Turn On Your Computer**
- Boot up your Windows computer
- Wait for the desktop to load completely

#### 2. **Start Ollama Service**
```powershell
# Open PowerShell as Administrator
# Start Ollama service (if not auto-starting)
ollama serve
```

#### 3. **Verify Ollama Models**
```powershell
# Check available models
ollama list

# If you need to pull a model (e.g., Mistral 7B)
ollama pull mistral:7b
```

#### 4. **Navigate to Project Directory**
```powershell
# Open PowerShell in your project directory
cd "c:\Users\vladi\AI Projects\blog-agent"
```

### **Phase 2: Blog Agent Setup**

#### 5. **Start the Blog Agent Services**
```powershell
# Option A: Use the batch file (easiest)
.\start_mcp.bat

# Option B: Manual startup
# Terminal 1: Start FastAPI server
uv run python main.py

# Terminal 2: Start MCP server
uv run python mcp_server.py
```

#### 6. **Verify Services Are Running**
```powershell
# Test the health endpoint
curl http://localhost:4891/health

# Test MCP server
echo '{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}' | uv run python mcp_server.py
```

### **Phase 3: VS Code Integration**

#### 7. **Open VS Code**
```powershell
# Open VS Code in the project directory
code .
```

#### 8. **Verify MCP Integration**
- Open Command Palette (`Ctrl+Shift+P`)
- Type "MCP: List Tools"
- Verify you see: `chat_completion`, `health_check`, `list_models`, `draft_post`

### **Phase 4: Generate Blog Post**

#### 9. **Method 1: Using Web Interface (Recommended)**
1. **Open your browser**
2. **Navigate to**: `http://localhost:4891/static/index.html`
3. **Fill out the form**:
   - **Topic**: "Getting Started with FastAPI and Ollama"
   - **Model**: "mistral:7b"
   - **Blog Folder**: "posts"
4. **Click "Generate Blog Post"**
5. **Wait for generation** (30-60 seconds)
6. **Review the results**:
   - Check content statistics
   - Review any content issues
   - Note the generated filename

#### 10. **Method 2: Using VS Code MCP Integration**
1. **Open Copilot Chat** (`Ctrl+Shift+I`)
2. **Type the command**:
   ```
   /draft_post topic="Getting Started with FastAPI and Ollama"
   ```
3. **Wait for generation**
4. **Review the response** with filename and preview

#### 11. **Method 3: Using Direct API Call**
```powershell
# Use curl to generate a post
curl -X POST "http://localhost:4891/tool/draft_post" \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Getting Started with FastAPI and Ollama",
    "model": "mistral:7b",
    "blog_folder": "posts"
  }'
```

### **Phase 5: Review & Edit Generated Post**

#### 12. **Locate the Generated File**
- **File Location**: `c:\Users\vladi\AI Projects\blog-agent\posts\`
- **Filename Format**: `YYYY-MM-DD-topic-slug.qmd`
- **Example**: `2025-07-09-getting-started-with-fastapi-and-ollama.qmd`

#### 13. **Open and Review the Post**
```powershell
# Open the generated file in VS Code
code "posts\2025-07-09-getting-started-with-fastapi-and-ollama.qmd"
```

#### 14. **Edit the Post (if needed)**
- **Review the YAML frontmatter**:
  ```yaml
  ---
  title: "Getting Started with FastAPI and Ollama"
  description: "A comprehensive guide to getting started with fastapi and ollama"
  author: "AI Assistant"
  date: "2025-07-09"
  categories: [blog, ai, guide]
  ---
  ```
- **Edit content** as needed
- **Add images** if required
- **Update metadata** (author, categories, etc.)

### **Phase 6: Test the Post Locally**

#### 15. **Preview with Quarto (if using Quarto)**
```powershell
# Install Quarto if not installed
# Then preview the post
quarto preview "posts\2025-07-09-getting-started-with-fastapi-and-ollama.qmd"
```

#### 16. **Test Markdown Rendering**
- **Open the file** in VS Code
- **Use Preview** (`Ctrl+Shift+V`)
- **Check formatting** and structure

### **Phase 7: Commit & Push Changes**

#### 17. **Check Git Status**
```powershell
# Check what files have changed
git status

# See the new file
git diff --name-only
```

#### 18. **Add the New Post**
```powershell
# Add the new post file
git add "posts\2025-07-09-getting-started-with-fastapi-and-ollama.qmd"

# Or add all changes
git add .
```

#### 19. **Commit the Changes**
```powershell
# Commit with descriptive message
git commit -m "Add new blog post: Getting Started with FastAPI and Ollama

- Generated using blog-agent with mistral:7b model
- Word count: ~1247 words
- Includes code examples and comprehensive guide
- Added on 2025-07-09"
```

#### 20. **Push to Repository**
```powershell
# Push to your main branch
git push origin main

# Or if using different branch
git push origin your-branch-name
```

### **Phase 8: Deploy & Verify Online**

#### 21. **Trigger Deployment**
- **GitHub Pages**: Automatic deployment after push
- **Netlify**: Automatic deployment after push
- **Vercel**: Automatic deployment after push
- **Custom Server**: Manual deployment if needed

#### 22. **Wait for Deployment**
- **Check deployment status** in your hosting platform
- **GitHub Actions**: Check the Actions tab
- **Netlify**: Check the Deploys tab
- **Vercel**: Check the Deployments tab

#### 23. **Verify the Post is Online**
1. **Open your browser**
2. **Navigate to your blog URL**
3. **Check the new post appears**:
   - In the blog index/home page
   - At the direct post URL
   - In any RSS feeds
4. **Test the post content**:
   - Verify formatting is correct
   - Check images load properly
   - Test any interactive elements

### **Phase 9: Final Verification**

#### 24. **Test Post Accessibility**
- **Check mobile responsiveness**
- **Test different browsers**
- **Verify SEO elements** (title, description, etc.)

#### 25. **Share & Promote**
- **Copy the post URL**
- **Share on social media** if desired
- **Update any relevant documentation**

## 🎉 Success Checklist

- ✅ Computer started and ready
- ✅ Ollama service running
- ✅ Blog-agent services started
- ✅ VS Code MCP integration working
- ✅ Blog post generated successfully
- ✅ Post content reviewed and edited
- ✅ Changes committed to Git
- ✅ Changes pushed to repository
- ✅ Deployment completed successfully
- ✅ Post verified online and accessible

## 🔧 Troubleshooting

### **Common Issues & Solutions**

#### **Ollama Not Responding**
```powershell
# Restart Ollama service
taskkill /f /im ollama.exe
ollama serve
```

#### **Blog Agent Services Not Starting**
```powershell
# Check port availability
netstat -ano | findstr :4891

# Kill any processes using the port
taskkill /f /pid <PID>
```

#### **MCP Integration Not Working**
- Restart VS Code
- Check MCP extensions are installed
- Verify mcp-manifest.json is correct

#### **Git Push Fails**
```powershell
# Check git status
git status

# Pull latest changes first
git pull origin main

# Then push again
git push origin main
```

#### **Deployment Issues**
- Check hosting platform logs
- Verify build configuration
- Check for any syntax errors in the post

## 📊 Performance Expectations

- **Blog Generation**: 30-60 seconds
- **Git Operations**: 5-10 seconds
- **Deployment**: 2-5 minutes
- **Total Process**: 5-10 minutes end-to-end

## 🎯 Tips for Success

1. **Keep Ollama running** in the background
2. **Use descriptive commit messages**
3. **Review generated content** before publishing
4. **Test locally** before pushing
5. **Monitor deployment** for issues
6. **Keep backups** of important posts

**You now have a complete workflow from computer startup to published blog post!** 🚀
