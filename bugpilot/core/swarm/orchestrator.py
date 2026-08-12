import json
from typing import Dict, Any, Optional
from bugpilot.core.terminal_ui import TerminalUI
from bugpilot.agent.executor import Executor
from bugpilot.core.swarm.roles import RoleManager
from bugpilot.core.llm.factory import ModelFactory
from bugpilot.agent.tools_schema import get_core_tools
from bugpilot.core.prompts import get_system_prompt

class SwarmOrchestrator:
    """Main Orchestrator Agent that manages Sub-Agents."""
    
    def __init__(self, main_model, config, ui: TerminalUI):
        self.main_model = main_model
        self.config = config
        self.ui = ui
        self.role_manager = RoleManager()
        self.executor = Executor(safety_config=config.safety)
        self.history = []
        
    def delegate_task(self, role_name: str, objective: str) -> str:
        """Spins up a specialized sub-agent to achieve a specific objective."""
        role = self.role_manager.get_role(role_name)
        if not role:
            return f"Error: Role '{role_name}' does not exist."
            
        self.ui.print_panel(f"Spinning up '{role.name}' agent...\nObjective: {objective}", title="Swarm Delegation", style="magenta")
        
        # Determine model for sub-agent
        model = self.main_model
        if role.model_override:
            # Example parsing: groq:llama-3.3-70b-versatile
            parts = role.model_override.split(":")
            if len(parts) == 2:
                provider, model_name = parts
                # Get key from config
                # In real scenario, we'd fetch the specific API key for that provider from config
                api_key = getattr(self.config, f"{provider}_api_key", None)
                try:
                    model = ModelFactory.create_model(provider, api_key=api_key, model_name=model_name)
                except Exception as e:
                    self.ui.print_warning(f"Failed to load override model {role.model_override}, using default.")
                    
        # Sub-agent loop
        return self._run_sub_agent(role, objective, model)
        
    def _run_sub_agent(self, role, objective: str, model) -> str:
        history = []
        all_tools = get_core_tools()
        # Filter tools to only what the role is allowed
        allowed_schemas = [t for t in all_tools if t["name"] in role.tools]
        
        system_msg = f"{role.system_prompt}\n\nYour objective: {objective}\nReturn your result using the ask_user tool when finished."
        
        MAX_ITER = 5
        for i in range(MAX_ITER):
            with self.ui.loading_indicator(f"[{role.name}] Thinking..."):
                prompt = system_msg + "\n\nOutput a strict JSON array of tool calls."
                try:
                    resp = model.generate(prompt, history)
                except Exception as e:
                    return f"Error communicating with LLM: {e}"
                    
            try:
                clean = resp.strip()
                if clean.startswith("```json"): clean = clean[7:]
                if clean.startswith("```"): clean = clean[3:]
                if clean.endswith("```"): clean = clean[:-3]
                tool_calls = json.loads(clean.strip())
                if isinstance(tool_calls, dict):
                    tool_calls = [tool_calls]
            except Exception:
                history.append({"role": "user", "content": "SYSTEM ERROR: Invalid JSON."})
                continue
                
            for call in tool_calls:
                t_name = call.get("tool")
                params = call.get("parameters", {})
                
                if t_name == "ask_user":
                    # Sub-agent finished
                    return params.get("prompt", "Done")
                    
                if t_name not in role.tools:
                    history.append({"role": "user", "content": f"SYSTEM ERROR: Tool {t_name} not allowed for your role."})
                    continue
                    
                # Execute simple command for now
                if t_name == "execute_command":
                    cmd = params.get("command")
                    with self.ui.loading_indicator(f"[{role.name}] Executing {cmd[:20]}..."):
                        res = self.executor.execute(cmd)
                    history.append({"role": "user", "content": f"Output: {res.get('output', '')[:1000]}"})
                
                # Mock others for now
                else:
                    history.append({"role": "user", "content": "Tool execution successful."})
                    
        return "Error: Sub-agent timed out."
