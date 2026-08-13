"""
Enhanced Input Module - Autocomplete for commands and files
"""

from prompt_toolkit import prompt
from prompt_toolkit.completion import Completer, Completion, PathCompleter
from prompt_toolkit.document import Document
from typing import List, Iterable
import os


class BugPilotCompleter(Completer):
    """Custom completer for BugPilot CLI with command and file suggestions"""
    
    COMMANDS = [
        "/help", "/theme", "/mode", "/model", "/output", "/autopilot",
        "/save", "/export", "/sessions", "/load", "/history",
        "/tokens", "/stream", "/reset", "/clear", "/exit", "/quit",
        "/update", "/cve", "/owasp", "/connect"
    ]
    
    def __init__(self, working_directory: str = ".", config_manager=None):
        self.working_directory = working_directory
        self.path_completer = PathCompleter(only_directories=False, expanduser=True)
        self.config_manager = config_manager
        self.model_cache = {}
    
    def get_completions(self, document: Document, complete_event) -> Iterable[Completion]:
        text = document.text_before_cursor
        
        # Command completion with /
        if text.startswith('/'):
            parts = text.split(' ')
            
            # Sub-command completion for /theme
            if parts[0] == '/theme':
                if len(parts) == 2:
                    themes = ['ocean', 'hacker', 'dracula', 'monokai', 'matrix', 'synthwave', 'nord']
                    word = parts[1]
                    for t in themes:
                        if t.startswith(word.lower()):
                            yield Completion(
                                t,
                                start_position=-len(word),
                                display=t,
                                display_meta="Theme"
                            )
                    return

            if parts[0] in ['/connect', '/model']:
                if len(parts) == 2:
                    providers = ['openai', 'gemini', 'claude', 'groq', 'ollama', 'openrouter', 'deepseek', 'nvidia']
                    word = parts[1]
                    for p in providers:
                        if p.startswith(word.lower()):
                            yield Completion(
                                p,
                                start_position=-len(word),
                                display=p,
                                display_meta="Provider"
                            )
                    return
                elif len(parts) == 3 and parts[0] == '/model':
                    provider = parts[1].lower()
                    word = parts[2]
                    
                    models = self._get_provider_models(provider)
                    for m in models:
                        if m.startswith(word.lower()):
                            yield Completion(
                                m,
                                start_position=-len(word),
                                display=m,
                                display_meta=f"{provider} model"
                            )
                    return

            if len(parts) == 1:
                word = text[1:]  # Remove the /
                for cmd in self.COMMANDS:
                    if cmd[1:].startswith(word.lower()):
                        yield Completion(
                            cmd[1:],  # Complete without /
                            start_position=-len(word),
                            display=cmd,
                            display_meta="Command"
                        )
        
        # File completion with @
        elif '@' in text:
            # Get text after last @
            parts = text.rsplit('@', 1)
            if len(parts) == 2:
                prefix, file_part = parts
                
                # Use PathCompleter for file suggestions
                try:
                    files = []
                    search_dir = self.working_directory
                    
                    # Get files in working directory
                    if os.path.exists(search_dir):
                        for item in os.listdir(search_dir):
                            item_path = os.path.join(search_dir, item)
                            if os.path.isfile(item_path) and item.lower().startswith(file_part.lower()):
                                files.append(item)
                    
                    for file in files[:10]:  # Limit to 10 suggestions
                        if file.startswith(file_part):
                            yield Completion(
                                file,
                                start_position=-len(file_part),
                                display=f"@{file}",
                                display_meta="File"
                            )
                except:
                    pass
        
        # Folder completion with #
        elif '#' in text:
            parts = text.rsplit('#', 1)
            if len(parts) == 2:
                prefix, folder_part = parts
                
                try:
                    folders = []
                    search_dir = self.working_directory
                    
                    if os.path.exists(search_dir):
                        for item in os.listdir(search_dir):
                            item_path = os.path.join(search_dir, item)
                            if os.path.isdir(item_path) and item.lower().startswith(folder_part.lower()):
                                folders.append(item)
                    
                    for folder in folders[:10]:
                        if folder.startswith(folder_part):
                            yield Completion(
                                folder,
                                start_position=-len(folder_part),
                                display=f"#{folder}",
                                display_meta="Folder"
                            )
                except:
                    pass

    def _get_provider_models(self, provider: str) -> List[str]:
        """Dynamically fetch models for a given provider or use fallbacks"""
        if provider in self.model_cache:
            return self.model_cache[provider]
            
        fallback_models = {
            "openai": ["gpt-4o", "gpt-4-turbo", "gpt-3.5-turbo"],
            "anthropic": ["claude-3-5-sonnet-20241022", "claude-3-opus-20240229"],
            "gemini": ["gemini-2.0-flash-exp", "gemini-1.5-pro"],
            "ollama": ["llama3", "mistral", "codellama"],
            "nvidia": ["meta/llama3-70b-instruct", "mistralai/mixtral-8x22b-instruct-v0.1"],
            "groq": ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"],
            "deepseek": ["deepseek-coder", "deepseek-chat"],
            "openrouter": ["anthropic/claude-3.5-sonnet", "meta-llama/llama-3-70b-instruct"]
        }
        
        if not self.config_manager:
            return fallback_models.get(provider, [])
            
        api_key = self.config_manager.get_api_key(provider)
        if not api_key and provider != "ollama":
            return fallback_models.get(provider, [])
            
        import requests
        try:
            url = ""
            headers = {"Authorization": f"Bearer {api_key}"}
            
            if provider == "openai":
                url = "https://api.openai.com/v1/models"
            elif provider == "nvidia":
                url = "https://integrate.api.nvidia.com/v1/models"
            elif provider == "groq":
                url = "https://api.groq.com/openai/v1/models"
            elif provider == "deepseek":
                url = "https://api.deepseek.com/models"
            elif provider == "openrouter":
                url = "https://openrouter.ai/api/v1/models"
            elif provider == "ollama":
                url = "http://localhost:11434/api/tags"
                headers = {}
                
            if url:
                resp = requests.get(url, headers=headers, timeout=1.0)
                if resp.status_code == 200:
                    data = resp.json()
                    if provider == "ollama":
                        models = [m["name"] for m in data.get("models", [])]
                    else:
                        models = [m["id"] for m in data.get("data", [])]
                        
                    if models:
                        self.model_cache[provider] = models
                        return models
        except Exception:
            pass
            
        models = fallback_models.get(provider, [])
        self.model_cache[provider] = models
        return models


def get_user_input_with_autocomplete(
    prompt_text: str,
    working_directory: str = ".",
    multiline: bool = False,
    **kwargs
) -> str:
    """
    Get user input with intelligent autocomplete
    
    Features:
    - /command - Shows command suggestions
    - @file - Shows file suggestions
    - #folder - Shows folder suggestions
    """
    completer = BugPilotCompleter(working_directory)
    
    try:
        result = prompt(
            prompt_text,
            completer=completer,
            complete_while_typing=True,
            multiline=multiline,
            **kwargs
        )
        return result
    except (KeyboardInterrupt, EOFError):
        return ""
    except Exception as e:
        # Fallback to regular input
        return input(prompt_text)


# Helper functions for specific use cases
def get_command_input(prompt_text: str = "[+] You: ", **kwargs) -> str:
    """Get input with command autocomplete"""
    return get_user_input_with_autocomplete(prompt_text, **kwargs)


def get_file_input(prompt_text: str, working_directory: str = ".") -> str:
    """Get input with file autocomplete"""
    return get_user_input_with_autocomplete(prompt_text, working_directory)
