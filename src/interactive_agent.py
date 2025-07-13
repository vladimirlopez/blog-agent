"""
Interactive Blog Writing Agent - Enhanced MCP Server for collaborative writing
"""

import asyncio
import json
import sys
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional
import httpx
from .schemas import ChatCompletionRequest, ChatCompletionResponse, DraftPostRequest, DraftPostResponse
from .ollama_client import OllamaClient

# Interactive writing session state
writing_sessions = {}

class InteractiveBlogAgent:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.ollama_client = OllamaClient(base_url)
        self.current_session = None
        
    def start_session(self, blog_folder: str, topic: str) -> str:
        """Start a new interactive writing session"""
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        writing_sessions[session_id] = {
            'blog_folder': blog_folder,
            'topic': topic,
            'content_sections': {},
            'current_draft': '',
            'conversation_history': [],
            'created_at': datetime.now().isoformat()
        }
        
        self.current_session = session_id
        return session_id
    
    async def chat_about_post(self, session_id: str, user_message: str, model: str = "mistral:7b") -> str:
        """Have a conversation about the blog post"""
        if session_id not in writing_sessions:
            return "Session not found. Please start a new session."
        
        session = writing_sessions[session_id]
        
        # Build context from conversation history
        context_messages = [
            {
                "role": "system", 
                "content": f"""You are an expert blog writing assistant. You're helping write a blog post about "{session['topic']}". 

Current draft content:
{session['current_draft'] if session['current_draft'] else 'No content yet'}

You should:
1. Help refine ideas and structure
2. Suggest content improvements
3. Write specific sections when asked
4. Provide feedback on existing content
5. Help with formatting and organization

Be conversational and collaborative. Ask clarifying questions when needed."""
            }
        ]
        
        # Add conversation history
        context_messages.extend(session['conversation_history'])
        
        # Add current user message
        context_messages.append({"role": "user", "content": user_message})
        
        # Get AI response
        chat_request = ChatCompletionRequest(
            model=model,
            messages=context_messages,
            temperature=0.7,
            max_tokens=1500
        )
        
        response = await self.ollama_client.chat_completion(chat_request)
        ai_response = response.choices[0].message.content
        
        # Update conversation history
        session['conversation_history'].append({"role": "user", "content": user_message})
        session['conversation_history'].append({"role": "assistant", "content": ai_response})
        
        return ai_response
    
    async def update_draft(self, session_id: str, content: str) -> str:
        """Update the current draft content"""
        if session_id not in writing_sessions:
            return "Session not found."
        
        session = writing_sessions[session_id]
        session['current_draft'] = content
        
        return "Draft updated successfully."
    
    async def save_draft(self, session_id: str, filename: Optional[str] = None) -> str:
        """Save the current draft to a file"""
        if session_id not in writing_sessions:
            return "Session not found."
        
        session = writing_sessions[session_id]
        
        if not session['current_draft']:
            return "No draft content to save."
        
        # Create filename if not provided
        if not filename:
            date_str = datetime.now().strftime("%Y-%m-%d")
            slug = session['topic'].lower().replace(' ', '-').replace(',', '').replace('.', '')
            filename = f"{date_str}-{slug}.md"
        
        # Ensure .md extension
        if not filename.endswith('.md'):
            filename += '.md'
        
        # Save to blog folder
        blog_folder = Path(session['blog_folder'])
        blog_folder.mkdir(parents=True, exist_ok=True)
        
        file_path = blog_folder / filename
        
        # Add frontmatter if not present
        content = session['current_draft']
        if not content.startswith('---'):
            frontmatter = f"""---
title: "{session['topic']}"
date: "{datetime.now().strftime('%Y-%m-%d')}"
draft: true
---

"""
            content = frontmatter + content
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return f"Draft saved to: {file_path}"
    
    def get_session_status(self, session_id: str) -> Dict[str, Any]:
        """Get current session status"""
        if session_id not in writing_sessions:
            return {"error": "Session not found"}
        
        session = writing_sessions[session_id]
        return {
            "session_id": session_id,
            "topic": session['topic'],
            "blog_folder": session['blog_folder'],
            "draft_length": len(session['current_draft']),
            "conversation_turns": len(session['conversation_history']) // 2,
            "created_at": session['created_at']
        }

# Global agent instance
interactive_agent = InteractiveBlogAgent()

async def _call_start_writing_session(args: Dict[str, Any]) -> Dict[str, Any]:
    """Start a new interactive writing session"""
    try:
        blog_folder = args.get('blog_folder', '.')
        topic = args.get('topic', 'New Blog Post')
        
        session_id = interactive_agent.start_session(blog_folder, topic)
        
        return {
            "session_id": session_id,
            "topic": topic,
            "blog_folder": blog_folder,
            "status": "Session started. You can now chat about your blog post!",
            "next_steps": [
                "Use chat_about_post to discuss ideas",
                "Use update_draft to modify content",
                "Use save_draft when ready to save"
            ]
        }
    except Exception as e:
        return {"error": f"Failed to start session: {str(e)}"}

async def _call_chat_about_post(args: Dict[str, Any]) -> Dict[str, Any]:
    """Chat about the blog post"""
    try:
        session_id = args.get('session_id', '')
        message = args.get('message', '')
        model = args.get('model', 'mistral:7b')
        
        if not session_id or not message:
            return {"error": "session_id and message are required"}
        
        response = await interactive_agent.chat_about_post(session_id, message, model)
        
        return {
            "response": response,
            "session_id": session_id
        }
    except Exception as e:
        return {"error": f"Chat failed: {str(e)}"}

async def _call_update_draft(args: Dict[str, Any]) -> Dict[str, Any]:
    """Update the current draft"""
    try:
        session_id = args.get('session_id', '')
        content = args.get('content', '')
        
        if not session_id:
            return {"error": "session_id is required"}
        
        result = await interactive_agent.update_draft(session_id, content)
        
        return {
            "result": result,
            "session_id": session_id
        }
    except Exception as e:
        return {"error": f"Update failed: {str(e)}"}

async def _call_save_draft(args: Dict[str, Any]) -> Dict[str, Any]:
    """Save the current draft"""
    try:
        session_id = args.get('session_id', '')
        filename = args.get('filename')
        
        if not session_id:
            return {"error": "session_id is required"}
        
        result = await interactive_agent.save_draft(session_id, filename)
        
        return {
            "result": result,
            "session_id": session_id
        }
    except Exception as e:
        return {"error": f"Save failed: {str(e)}"}

async def _call_get_session_status(args: Dict[str, Any]) -> Dict[str, Any]:
    """Get session status"""
    try:
        session_id = args.get('session_id', '')
        
        if not session_id:
            return {"error": "session_id is required"}
        
        return interactive_agent.get_session_status(session_id)
    except Exception as e:
        return {"error": f"Status check failed: {str(e)}"}

# Add these tools to the main MCP server tools list
INTERACTIVE_TOOLS = {
    "start_writing_session": _call_start_writing_session,
    "chat_about_post": _call_chat_about_post,
    "update_draft": _call_update_draft,
    "save_draft": _call_save_draft,
    "get_session_status": _call_get_session_status
}
