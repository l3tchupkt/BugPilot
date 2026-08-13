"""Interactive Settings Editor - Rich-based UI"""

import os
import yaml
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich import box


class SettingsEditor:
    """Interactive settings editor with Rich UI"""
    
    def __init__(self):
        self.settings_path = Path(__file__).parent / "settings.yaml"
        self.console = Console()
        self.settings = self.load_settings()
    
    def load_settings(self) -> dict:
        """Load settings from package"""
        if not self.settings_path.exists():
            # Create from defaults
            defaults = Path(__file__).parent / "defaults.yaml"
            if defaults.exists():
                import shutil
                shutil.copy(defaults, self.settings_path)
        
        with open(self.settings_path, 'r') as f:
            return yaml.safe_load(f) or {}
    
    def save_settings(self):
        """Save settings with error handling"""
        try:
            with open(self.settings_path, 'w') as f:
                yaml.dump(self.settings, f, default_flow_style=False, sort_keys=False)
            self.console.print("\n[green]Settings saved successfully![/green]")
        except PermissionError:
            self.console.print("\n[red]Error: Permission denied saving settings.yaml[/red]")
            self.console.print("[yellow]Try running as Administrator/Root to save package settings.[/yellow]")
            Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")
        except Exception as e:
            self.console.print(f"\n[red]Error saving settings: {e}[/red]")
            Prompt.ask("\n[dim]Press Enter to continue[/dim]", default="")
    
    def show_menu(self):
        """Main settings menu"""
        from prompt_toolkit.shortcuts import radiolist_dialog, yes_no_dialog
        
        while True:
            choice = radiolist_dialog(
                title="BugPilot Settings",
                text="Configure everything here",
                values=[
                    ("1", "Connect Provider"),
                    ("2", "Models"),
                    ("3", "Parameters"),
                    ("4", "Safety & Limits"),
                    ("5", "Modes (Forge/Hacker)"),
                    ("6", "UI Preferences"),
                    ("7", "Context & Session"),
                    ("8", "View All Settings"),
                    ("s", "Save & Return"),
                ],
                cancel_text="Exit"
            ).run()
            
            if choice is None:
                if yes_no_dialog(title="Confirm", text="Discard changes?").run():
                    break
                else:
                    continue
            
            if choice == "1":
                self.edit_api_keys()
            elif choice == "2":
                self.edit_models()
            elif choice == "3":
                self.edit_parameters()
            elif choice == "4":
                self.edit_safety()
            elif choice == "5":
                self.edit_modes()
            elif choice == "6":
                self.edit_ui()
            elif choice == "7":
                self.edit_context_session()
            elif choice == "8":
                self.view_all()
            elif choice.lower() == "s":
                self.save_settings()
                break
    
    def _fetch_models(self, provider: str, api_key: str = None) -> list:
        """Fetch models dynamically for a provider"""
        models = []
        try:
            self.console.print(f"[dim]Fetching models for {provider}...[/dim]")
            if provider == "gemini":
                try:
                    import google.generativeai as genai
                    genai.configure(api_key=api_key)
                    models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                except Exception as e:
                    self.console.print(f"[red]Gemini fetch error: {e}[/red]")
            elif provider == "groq":
                try:
                    from groq import Groq
                    client = Groq(api_key=api_key)
                    models = [m.id for m in client.models.list().data]
                except Exception as e:
                    self.console.print(f"[red]Groq fetch error: {e}[/red]")
            elif provider == "openai":
                try:
                    from openai import OpenAI
                    client = OpenAI(api_key=api_key)
                    models = [m.id for m in client.models.list().data]
                except Exception as e:
                    self.console.print(f"[red]OpenAI fetch error: {e}[/red]")
            elif provider == "claude":
                try:
                    import anthropic
                    client = anthropic.Anthropic(api_key=api_key)
                    models = [m.id for m in client.models.list().data]
                except Exception as e:
                    self.console.print(f"[red]Claude fetch error: {e}[/red]")
                    # Fallback for Claude if list is not supported
                    if not models:
                        models = ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307", "claude-3-5-sonnet-20241022", "claude-3-5-haiku-20241022"]
            elif provider == "ollama":
                try:
                    import requests
                    url = api_key if api_key else "http://localhost:11434"
                    response = requests.get(f"{url}/api/tags", timeout=5)
                    response.raise_for_status()
                    models = [m["name"] for m in response.json().get("models", [])]
                except Exception as e:
                    self.console.print(f"[red]Ollama fetch error: {e}[/red]")
        except Exception as e:
            self.console.print(f"[red]Error fetching models: {e}[/red]")
        
        return models

    def edit_api_keys(self):
        """Connect Provider"""
        from prompt_toolkit.shortcuts import radiolist_dialog, input_dialog, message_dialog
        
        if 'api_keys' not in self.settings:
            self.settings['api_keys'] = {}
        if 'models_cache' not in self.settings:
            self.settings['models_cache'] = {}
        
        providers = [
            ('gemini', 'Gemini'),
            ('groq', 'Groq'),
            ('openai', 'OpenAI'),
            ('claude', 'Claude (Anthropic)'),
            ('ollama', 'Ollama (Local)'),
            ('openrouter', 'OpenRouter'),
            ('deepseek', 'DeepSeek'),
            ('nvidia', 'Nvidia (NIM)')
        ]
        
        values = []
        for provider, name in providers:
            current = self.settings['api_keys'].get(provider, '')
            if provider == 'ollama':
                status = f"Set ({current or 'http://localhost:11434'})" if current else "Not set"
            else:
                status = "Set" if current else "Not set"
            values.append((provider, f"{name}: {status}"))
            
        choice = radiolist_dialog(
            title="Connect Provider",
            text="Select a provider to connect:",
            values=values
        ).run()
        
        if choice:
            name = dict(providers).get(choice)
            if choice == 'ollama':
                api_key = input_dialog(
                    title=f"Connect {name}",
                    text=f"Enter {name} Base URL:",
                    default="http://localhost:11434"
                ).run()
            else:
                api_key = input_dialog(
                    title=f"Connect {name}",
                    text=f"Enter {name} API key:",
                    password=True
                ).run()
                
            if api_key:
                self.settings['api_keys'][choice] = api_key
                models = self._fetch_models(choice, api_key)
                if models:
                    self.settings['models_cache'][choice] = models
                    message_dialog(
                        title="Success",
                        text=f"{name} connected successfully! Fetched {len(models)} models."
                    ).run()
                else:
                    message_dialog(
                        title="Warning",
                        text="Could not fetch models. They may not be available or the key/URL is invalid."
                    ).run()
    
    def edit_models(self):
        """Select Model"""
        from prompt_toolkit.shortcuts import radiolist_dialog, input_dialog, message_dialog
        
        if 'llm' not in self.settings:
            self.settings['llm'] = {}
            
        connected_providers = [p for p, k in self.settings.get('api_keys', {}).items() if k]
        
        if not connected_providers:
            message_dialog(title="Select Model", text="No providers connected. Please connect a provider first.").run()
            return
            
        provider_values = [(p, p.capitalize()) for p in connected_providers]
        selected_provider = radiolist_dialog(
            title="Select Provider",
            text="Choose a connected provider:",
            values=provider_values
        ).run()
        
        if not selected_provider:
            return
            
        self.settings['llm']['default_provider'] = selected_provider
        
        models_cache = self.settings.get('models_cache', {}).get(selected_provider, [])
        if not models_cache:
            api_key = self.settings['api_keys'].get(selected_provider)
            models_cache = self._fetch_models(selected_provider, api_key)
            if 'models_cache' not in self.settings:
                self.settings['models_cache'] = {}
            self.settings['models_cache'][selected_provider] = models_cache
            
        if models_cache:
            model_values = [(m, m) for m in models_cache]
            selected_model = radiolist_dialog(
                title="Select Model",
                text=f"Available Models for {selected_provider.capitalize()}:",
                values=model_values
            ).run()
            
            if selected_model:
                if 'models' not in self.settings['llm']:
                    self.settings['llm']['models'] = {}
                if 'reasoning' not in self.settings['llm']['models']:
                    self.settings['llm']['models']['reasoning'] = {}
                    
                self.settings['llm']['models']['reasoning']['model'] = selected_model
                message_dialog(title="Success", text=f"Selected model: {selected_model} for {selected_provider}").run()
        else:
            fallback_model = input_dialog(
                title="Select Model",
                text=f"Could not load models for {selected_provider}.\nEnter model manually (e.g. gpt-4o):"
            ).run()
            
            if fallback_model:
                if 'models' not in self.settings['llm']:
                    self.settings['llm']['models'] = {}
                if 'reasoning' not in self.settings['llm']['models']:
                    self.settings['llm']['models']['reasoning'] = {}
                self.settings['llm']['models']['reasoning']['model'] = fallback_model
                message_dialog(title="Success", text=f"Selected model: {fallback_model} for {selected_provider}").run()

    def edit_parameters(self):
        """Edit LLM Parameters"""
        from prompt_toolkit.shortcuts import input_dialog
        
        if 'llm' not in self.settings:
            self.settings['llm'] = {}
            
        temp = input_dialog(
            title="LLM Parameters",
            text="Temperature (0.0 - 1.0):",
            default=str(self.settings['llm'].get('temperature', 0.7))
        ).run()
        
        if temp is not None:
            try:
                self.settings['llm']['temperature'] = float(temp)
            except ValueError:
                pass
            
        max_tokens = input_dialog(
            title="LLM Parameters",
            text="Max Tokens:",
            default=str(self.settings['llm'].get('max_tokens', 8192))
        ).run()
        
        if max_tokens is not None:
            try:
                self.settings['llm']['max_tokens'] = int(max_tokens)
            except ValueError:
                pass
    
    def edit_context_session(self):
        """Edit session settings"""
        from prompt_toolkit.shortcuts import input_dialog, yes_no_dialog
        
        # Context settings have been removed as per user request to handle dynamic unlimited context
        
        # Session
        if 'session' not in self.settings:
            self.settings['session'] = {}
            
        auto_save = yes_no_dialog(
            title="Session Management",
            text="Auto-save sessions?"
        ).run()
        if auto_save is not None:
            self.settings['session']['auto_save'] = auto_save
        
        save_dir = input_dialog(
            title="Session Management",
            text="Session Save Directory:",
            default=self.settings['session'].get('save_dir', '.bugpilot_sessions')
        ).run()
        if save_dir is not None:
            self.settings['session']['save_dir'] = save_dir
    
    def view_all(self):
        """View all settings"""
        from prompt_toolkit.shortcuts import message_dialog
        
        # Mask API keys
        display_settings = self.settings.copy()
        if 'api_keys' in display_settings:
            for key in display_settings['api_keys']:
                val = display_settings['api_keys'][key]
                if val:
                    display_settings['api_keys'][key] = val[:8] + "..." if len(val) > 8 else "***"
        
        settings_text = yaml.dump(display_settings, default_flow_style=False)
        message_dialog(
            title="Current Settings",
            text=settings_text
        ).run()

    def edit_safety(self):
        """Edit safety settings"""
        from prompt_toolkit.shortcuts import input_dialog, yes_no_dialog
        
        if 'safety' not in self.settings:
            self.settings['safety'] = {}
        
        require_conf = yes_no_dialog(
            title="Safety Settings",
            text="Require confirmation before executing commands?"
        ).run()
        
        if require_conf is not None:
            self.settings['safety']['require_confirmation'] = require_conf
        
        max_calls = input_dialog(
            title="Safety Settings",
            text="Max tool calls per session:",
            default=str(self.settings['safety'].get('max_tool_calls', 10))
        ).run()
        if max_calls is not None:
            try:
                self.settings['safety']['max_tool_calls'] = int(max_calls)
            except ValueError:
                pass
        
        timeout = input_dialog(
            title="Safety Settings",
            text="Command timeout (seconds):",
            default=str(self.settings['safety'].get('timeout_seconds', 90))
        ).run()
        if timeout is not None:
            try:
                self.settings['safety']['timeout_seconds'] = int(timeout)
            except ValueError:
                pass
    
    def edit_modes(self):
        """Edit mode configuration"""
        from prompt_toolkit.shortcuts import radiolist_dialog, input_dialog
        
        if 'modes' not in self.settings:
            self.settings['modes'] = {}
        
        default_mode = radiolist_dialog(
            title="Modes Configuration",
            text="Default mode:",
            values=[("forge", "Forge"), ("hacker", "Hacker")],
        ).run()
        
        if default_mode:
            self.settings['modes']['default'] = default_mode
        
        # Forge mode
        if 'forge' not in self.settings['modes']:
            self.settings['modes']['forge'] = {}
        
        max_steps = input_dialog(
            title="Forge Mode Settings",
            text="Max steps:",
            default=str(self.settings['modes']['forge'].get('max_steps', 3))
        ).run()
        if max_steps is not None:
            try:
                self.settings['modes']['forge']['max_steps'] = int(max_steps)
            except ValueError:
                pass
        
        # Hacker mode
        if 'hacker' not in self.settings['modes']:
            self.settings['modes']['hacker'] = {}
        
        max_iter = input_dialog(
            title="Hacker Mode Settings",
            text="Max iterations:",
            default=str(self.settings['modes']['hacker'].get('max_iterations', 20))
        ).run()
        if max_iter is not None:
            try:
                self.settings['modes']['hacker']['max_iterations'] = int(max_iter)
            except ValueError:
                pass
    
    def edit_ui(self):
        """Edit UI preferences"""
        from prompt_toolkit.shortcuts import radiolist_dialog, input_dialog, yes_no_dialog
        
        if 'ui' not in self.settings:
            self.settings['ui'] = {}
        
        current_theme = self.settings['ui'].get('theme', 'ocean')
        themes = ["ocean", "sunset", "neon", "forest", "midnight", "cyber", "minimal"]
        theme = radiolist_dialog(
            title="UI Preferences",
            text="Select theme:",
            values=[(t, t.capitalize()) for t in themes]
        ).run()
        
        if theme:
            self.settings['ui']['theme'] = theme
        
        show_status = yes_no_dialog(
            title="UI Preferences",
            text="Show status bar?"
        ).run()
        if show_status is not None:
            self.settings['ui']['show_status_bar'] = show_status
        
        typing_effect = yes_no_dialog(
            title="UI Preferences",
            text="Enable typing effect?"
        ).run()
        if typing_effect is not None:
            self.settings['ui']['typing_effect'] = typing_effect
        
        if typing_effect:
            typing_speed = input_dialog(
                title="UI Preferences",
                text="Typing speed (characters per second):",
                default=str(self.settings['ui'].get('typing_speed', 150))
            ).run()
            if typing_speed is not None:
                try:
                    self.settings['ui']['typing_speed'] = int(typing_speed)
                except ValueError:
                    pass
        
        md_rendering = yes_no_dialog(
            title="UI Preferences",
            text="Enable markdown rendering?"
        ).run()
        if md_rendering is not None:
            self.settings['ui']['markdown_rendering'] = md_rendering
    

