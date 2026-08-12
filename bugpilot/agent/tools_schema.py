"""Tool Definitions for Function Calling"""
import json

def get_core_tools():
    """Returns the JSON schema definitions for native tool calling"""
    return [
        {
            "name": "execute_command",
            "description": "Execute a shell command on the host OS. The output will be automatically truncated if it exceeds safe lengths. For tools that support it (like nmap, nuclei), strongly prefer flags that output JSON.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The shell command to execute."
                    },
                    "timeout": {
                        "type": "integer",
                        "description": "Optional timeout in seconds.",
                        "default": 300
                    }
                },
                "required": ["command"]
            }
        },
        {
            "name": "read_file",
            "description": "Read the contents of a file on the host OS.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "Absolute or relative path to the file."
                    }
                },
                "required": ["filepath"]
            }
        },
        {
            "name": "write_file",
            "description": "Write contents to a file on the host OS.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filepath": {
                        "type": "string",
                        "description": "Path to the file to create or overwrite."
                    },
                    "content": {
                        "type": "string",
                        "description": "The content to write to the file."
                    }
                },
                "required": ["filepath", "content"]
            }
        },
        {
            "name": "web_search",
            "description": "Search the internet for vulnerability reports, exploits, documentation, or general queries using DuckDuckGo.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query."
                    }
                },
                "required": ["query"]
            }
        },
        {
            "name": "read_url",
            "description": "Fetch and extract text content from a specific URL. Useful after searching to read the full article or documentation.",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The full HTTP/HTTPS URL to fetch."
                    }
                },
                "required": ["url"]
            }
        },
        {
            "name": "ask_user",
            "description": "Halt autonomous execution and ask the user a question or for permission/clarification.",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt": {
                        "type": "string",
                        "description": "The message/question to show to the user."
                    }
                },
                "required": ["prompt"]
            }
        },
        {
            "name": "cve_search",
            "description": "Search the internal knowledge base for CVE information.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "CVE ID or search terms (e.g., 'apache 2.4.49')."
                    }
                },
                "required": ["query"]
            }
        },
        {
            "name": "owasp_info",
            "description": "Get details about an OWASP Top 10 category.",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "OWASP category code (e.g., 'A01', 'A03')."
                    }
                },
                "required": ["category"]
            }
        }
    ]
