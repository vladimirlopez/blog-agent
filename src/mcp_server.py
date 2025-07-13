#!/usr/bin/env python3
"""
MCP Server for Ollama Chat API
Provides Model Context Protocol server functionality for VS Code integration
"""

import asyncio
import json
import sys
import os
from typing import Any, Dict, List, Optional, Sequence
import httpx
from pydantic import BaseModel
from .interactive_agent import INTERACTIVE_TOOLS

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from .schemas import ChatCompletionRequest, ChatMessage


class MCPServer:
    """MCP Server for Ollama Chat API integration"""
    
    def __init__(self, base_url: str = "http://localhost:4891"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=120.0)
        # Store the active session ID for simplified chat commands
        self.active_session_id: Optional[str] = None
    
    async def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Handle incoming MCP requests"""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")
        
        try:
            if method == "initialize":
                return await self._handle_initialize(request_id, params)
            elif method == "tools/list":
                return await self._handle_list_tools(request_id)
            elif method == "tools/call":
                return await self._handle_tool_call(request_id, params)
            elif method == "resources/list":
                return await self._handle_list_resources(request_id)
            elif method == "resources/read":
                return await self._handle_read_resource(request_id, params)
            elif method == "prompts/list":
                return await self._handle_list_prompts(request_id)
            elif method == "prompts/get":
                return await self._handle_get_prompt(request_id, params)
            else:
                return self._error_response(request_id, -32601, f"Method not found: {method}")
        
        except Exception as e:
            return self._error_response(request_id, -32603, f"Internal error: {str(e)}")
    
    async def _handle_initialize(self, request_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle initialization request"""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": True,
                    "resources": True,
                    "prompts": True
                },
                "serverInfo": {
                    "name": "ollama-chat-api",
                    "version": "1.0.0"
                }
            }
        }
    
    async def _handle_list_tools(self, request_id: str) -> Dict[str, Any]:
        """List available tools"""
        tools = [
            {
                "name": "chat_completion",
                "description": "Generate chat completion using Ollama models",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "model": {"type": "string", "description": "Model to use"},
                        "messages": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "role": {"type": "string", "enum": ["system", "user", "assistant"]},
                                    "content": {"type": "string"}
                                },
                                "required": ["role", "content"]
                            }
                        },
                        "temperature": {"type": "number", "minimum": 0, "maximum": 2, "default": 0.7},
                        "max_tokens": {"type": "integer", "minimum": 1, "default": 150},
                        "stream": {"type": "boolean", "default": False}
                    },
                    "required": ["model", "messages"]
                }
            },
            {
                "name": "health_check",
                "description": "Check API health status",
                "inputSchema": {"type": "object", "properties": {}}
            },
            {
                "name": "list_models",
                "description": "List available models",
                "inputSchema": {"type": "object", "properties": {}}
            },
            {
                "name": "draft_post",
                "description": "Generate a Quarto blog post draft",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "topic": {"type": "string", "description": "The topic for the blog post"},
                        "model": {"type": "string", "default": "mistral:7b", "description": "Model to use for generation"},
                        "blog_folder": {"type": "string", "default": "posts", "description": "Target folder for blog posts"}
                    },
                    "required": ["topic"]
                }
            },
            {
                "name": "start_writing_session",
                "description": "Start an interactive blog writing session",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "blog_folder": {"type": "string", "description": "Path to your blog folder", "default": "."},
                        "topic": {"type": "string", "description": "Blog post topic"}
                    },
                    "required": ["topic"]
                }
            },
            {
                "name": "chat_about_post",
                "description": "Chat with AI about your blog post",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "session_id": {"type": "string", "description": "Writing session ID"},
                        "message": {"type": "string", "description": "Your message to the AI"},
                        "model": {"type": "string", "default": "mistral:7b"}
                    },
                    "required": ["session_id", "message"]
                }
            },
            {
                "name": "chat",
                "description": "Chat with AI about your current writing session (uses active session)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "message": {"type": "string", "description": "Your message to the AI"},
                        "model": {"type": "string", "default": "mistral:7b"}
                    },
                    "required": ["message"]
                }
            },
            {
                "name": "update_draft",
                "description": "Update the current blog post draft",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "session_id": {"type": "string", "description": "Writing session ID"},
                        "content": {"type": "string", "description": "New draft content"}
                    },
                    "required": ["session_id", "content"]
                }
            },
            {
                "name": "save_draft",
                "description": "Save the current draft to a file",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "session_id": {"type": "string", "description": "Writing session ID"},
                        "filename": {"type": "string", "description": "Optional filename"}
                    },
                    "required": ["session_id"]
                }
            },
            {
                "name": "get_session_status",
                "description": "Get current writing session status",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "session_id": {"type": "string", "description": "Writing session ID"}
                    },
                    "required": ["session_id"]
                }
            },
            {
                "name": "update",
                "description": "Update the current draft (uses active session)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "content": {"type": "string", "description": "New draft content"}
                    },
                    "required": ["content"]
                }
            },
            {
                "name": "save",
                "description": "Save the current draft to a file (uses active session)",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "filename": {"type": "string", "description": "Optional filename"}
                    }
                }
            },
            {
                "name": "status",
                "description": "Get current writing session status (uses active session)",
                "inputSchema": {
                    "type": "object",
                    "properties": {}
                }
            }
        ]
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"tools": tools}
        }
    
    async def _handle_tool_call(self, request_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tool call requests"""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if tool_name == "chat_completion":
            return await self._call_chat_completion(request_id, arguments)
        elif tool_name == "health_check":
            return await self._call_health_check(request_id)
        elif tool_name == "list_models":
            return await self._call_list_models(request_id)
        elif tool_name == "draft_post":
            return await self._call_draft_post(request_id, arguments)
        elif tool_name == "start_writing_session":
            return await self._call_start_writing_session(request_id, arguments)
        elif tool_name == "chat_about_post":
            return await self._call_chat_about_post(request_id, arguments)
        elif tool_name == "chat":
            return await self._call_chat(request_id, arguments)
        elif tool_name == "update_draft":
            return await self._call_update_draft(request_id, arguments)
        elif tool_name == "save_draft":
            return await self._call_save_draft(request_id, arguments)
        elif tool_name == "get_session_status":
            return await self._call_get_session_status(request_id, arguments)
        elif tool_name == "update":
            return await self._call_update(request_id, arguments)
        elif tool_name == "save":
            return await self._call_save(request_id, arguments)
        elif tool_name == "status":
            return await self._call_status(request_id, arguments)
        else:
            return self._error_response(request_id, -32602, f"Unknown tool: {tool_name}")
    
    async def _call_chat_completion(self, request_id: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call chat completion endpoint"""
        try:
            response = await self.client.post(
                f"{self.base_url}/v1/chat/completions",
                json=arguments
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{
                            "type": "text",
                            "text": result["choices"][0]["message"]["content"]
                        }]
                    }
                }
            else:
                return self._error_response(request_id, -32603, f"API error: {response.status_code}")
        
        except Exception as e:
            return self._error_response(request_id, -32603, f"Request failed: {str(e)}")
    
    async def _call_health_check(self, request_id: str) -> Dict[str, Any]:
        """Call health check endpoint"""
        try:
            response = await self.client.get(f"{self.base_url}/health")
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{
                            "type": "text",
                            "text": f"Health Status: {result.get('status', 'unknown')}"
                        }]
                    }
                }
            else:
                return self._error_response(request_id, -32603, f"Health check failed: {response.status_code}")
        
        except Exception as e:
            return self._error_response(request_id, -32603, f"Health check error: {str(e)}")
    
    async def _call_list_models(self, request_id: str) -> Dict[str, Any]:
        """Call list models endpoint"""
        try:
            response = await self.client.get(f"{self.base_url}/v1/models")
            
            if response.status_code == 200:
                result = response.json()
                models = [model["id"] for model in result.get("data", [])]
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{
                            "type": "text",
                            "text": f"Available models: {', '.join(models)}"
                        }]
                    }
                }
            else:
                return self._error_response(request_id, -32603, f"Models list failed: {response.status_code}")
        
        except Exception as e:
            return self._error_response(request_id, -32603, f"Models list error: {str(e)}")
    
    async def _call_draft_post(self, request_id: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call draft post endpoint"""
        try:
            response = await self.client.post(
                f"{self.base_url}/tool/draft_post",
                json=arguments
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "content": [{
                            "type": "text",
                            "text": f"✅ Blog post draft created!\n\nFilename: {result['filename']}\nPath: {result['full_path']}\n\nPreview:\n{result['preview']}"
                        }]
                    }
                }
            else:
                return self._error_response(request_id, -32603, f"Draft post creation failed: {response.status_code}")
        
        except Exception as e:
            return self._error_response(request_id, -32603, f"Draft post error: {str(e)}")
    
    async def _call_start_writing_session(self, request_id: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Start a new interactive writing session"""
        try:
            result = await INTERACTIVE_TOOLS["start_writing_session"](args)
            
            # Store the session ID as the active session for simplified commands
            if isinstance(result, dict) and "session_id" in result:
                self.active_session_id = result["session_id"]
            
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": result
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
            }

    async def _call_chat_about_post(self, request_id: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Chat about the blog post"""
        try:

            result = await INTERACTIVE_TOOLS["chat_about_post"](args)
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": result
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
            }

    async def _call_chat(self, request_id: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Chat with AI using the active session (simplified command)"""
        try:
            # Check if we have an active session
            if not self.active_session_id:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32602,
                        "message": "No active writing session. Please start a session first with /start_writing_session"
                    }
                }
            
            # Add the active session ID to the arguments
            chat_args = {
                "session_id": self.active_session_id,
                **args
            }
            
            # Call the existing chat_about_post function
            result = await INTERACTIVE_TOOLS["chat_about_post"](chat_args)
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": result
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
            }

    async def _call_update_draft(self, request_id: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Update the current draft"""
        try:

            result = await INTERACTIVE_TOOLS["update_draft"](args)
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": result
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
            }

    async def _call_save_draft(self, request_id: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Save the current draft"""
        try:

            result = await INTERACTIVE_TOOLS["save_draft"](args)
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": result
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
            }

    async def _call_get_session_status(self, request_id: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get session status"""
        try:

            result = await INTERACTIVE_TOOLS["get_session_status"](args)
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": result
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
            }

    async def _call_update(self, request_id: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Update draft using the active session (simplified command)"""
        try:
            if not self.active_session_id:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32602,
                        "message": "No active writing session. Please start a session first with /start_writing_session"
                    }
                }
            
            update_args = {
                "session_id": self.active_session_id,
                **args
            }
            
            result = await INTERACTIVE_TOOLS["update_draft"](update_args)
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": result
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
            }

    async def _call_save(self, request_id: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Save draft using the active session (simplified command)"""
        try:
            if not self.active_session_id:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32602,
                        "message": "No active writing session. Please start a session first with /start_writing_session"
                    }
                }
            
            save_args = {
                "session_id": self.active_session_id,
                **args
            }
            
            result = await INTERACTIVE_TOOLS["save_draft"](save_args)
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": result
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
            }

    async def _call_status(self, request_id: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Get session status using the active session (simplified command)"""
        try:
            if not self.active_session_id:
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "error": {
                        "code": -32602,
                        "message": "No active writing session. Please start a session first with /start_writing_session"
                    }
                }
            
            status_args = {
                "session_id": self.active_session_id,
                **args
            }
            
            result = await INTERACTIVE_TOOLS["get_session_status"](status_args)
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "result": result
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32603, "message": f"Internal error: {str(e)}"}
            }

    async def _handle_list_resources(self, request_id: str) -> Dict[str, Any]:
        """List available resources"""
        resources = [
            {
                "uri": f"{self.base_url}/v1/chat/completions",
                "name": "chat_completions",
                "description": "OpenAI-compatible chat completions endpoint",
                "mimeType": "application/json"
            },
            {
                "uri": f"{self.base_url}/health",
                "name": "health",
                "description": "Health check endpoint",
                "mimeType": "application/json"
            },
            {
                "uri": f"{self.base_url}/v1/models",
                "name": "models",
                "description": "List available models",
                "mimeType": "application/json"
            }
        ]
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"resources": resources}
        }
    
    async def _handle_read_resource(self, request_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Read a specific resource"""
        uri = params.get("uri")
        
        try:
            response = await self.client.get(uri)
            
            if response.status_code == 200:
                content = response.json()
                return {
                    "jsonrpc": "2.0",
                    "id": request_id,
                    "result": {
                        "contents": [{
                            "uri": uri,
                            "mimeType": "application/json",
                            "text": json.dumps(content, indent=2)
                        }]
                    }
                }
            else:
                return self._error_response(request_id, -32603, f"Resource read failed: {response.status_code}")
        
        except Exception as e:
            return self._error_response(request_id, -32603, f"Resource read error: {str(e)}")
    
    async def _handle_list_prompts(self, request_id: str) -> Dict[str, Any]:
        """List available prompts"""
        prompts = [
            {
                "name": "system_prompt",
                "description": "Default system prompt for chat completions",
                "arguments": [
                    {
                        "name": "role",
                        "description": "The role context for the assistant",
                        "required": False
                    }
                ]
            },
            {
                "name": "code_assistant",
                "description": "System prompt for code-related tasks",
                "arguments": [
                    {
                        "name": "language",
                        "description": "Programming language context",
                        "required": False
                    }
                ]
            }
        ]
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {"prompts": prompts}
        }
    
    async def _handle_get_prompt(self, request_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Get a specific prompt"""
        prompt_name = params.get("name")
        arguments = params.get("arguments", {})
        
        if prompt_name == "system_prompt":
            role = arguments.get("role", "helpful assistant")
            content = f"You are a {role}. Please provide helpful, accurate, and detailed responses."
        elif prompt_name == "code_assistant":
            language = arguments.get("language", "python")
            content = f"You are a {language} programming assistant. Help with code analysis, debugging, and implementation."
        else:
            return self._error_response(request_id, -32602, f"Unknown prompt: {prompt_name}")
        
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "result": {
                "description": f"Generated prompt: {prompt_name}",
                "messages": [
                    {
                        "role": "system",
                        "content": {"type": "text", "text": content}
                    }
                ]
            }
        }
    
    def _error_response(self, request_id: str, code: int, message: str) -> Dict[str, Any]:
        """Generate error response"""
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {
                "code": code,
                "message": message
            }
        }
    
    async def run(self):
        """Run the MCP server"""
        while True:
            try:
                line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
                if not line:
                    break
                
                request = json.loads(line.strip())
                response = await self.handle_request(request)
                
                print(json.dumps(response))
                sys.stdout.flush()
                
            except json.JSONDecodeError:
                continue
            except Exception as e:
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32700,
                        "message": f"Parse error: {str(e)}"
                    }
                }
                print(json.dumps(error_response))
                sys.stdout.flush()


async def main():
    """Main entry point"""
    server = MCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
