"""Hacker Mode - Autonomous pentesting (Unified Session)"""

import time
import re
import json
import os
from typing import List, Dict
from bugpilot.core.prompts import get_system_prompt
from bugpilot.core.state.session import SessionManager
from bugpilot.core.state.memory import DynamicContext
from bugpilot.agent.tools_schema import get_core_tools

class HackerMode:
    """Advanced autonomous mode - Persistent Session using Tool Calling logic"""
    
    def __init__(self, controller, ui, config):
        self.controller = controller
        self.ui = ui
        self.config = config
        self.session_manager = SessionManager()
        self.dynamic_context = DynamicContext()
        
        # Persistent State
        self.history = []
        self.todos = []
        self.findings = []
        self.iteration = 0
    
    def truncate_output(self, output: str, max_length: int = 5000) -> str:
        """Truncate massive outputs to save context window"""
        if not output: return ""
        if len(output) <= max_length:
            return output
        return output[:max_length//2] + f"\n\n... [TRUNCATED {len(output) - max_length} chars] ...\n\n" + output[-max_length//2:]
        
    def chat(self, user_input: str):
        """Process user input and loop autonomously until input needed"""
        from bugpilot.tools.knowledge import search_cve, get_owasp_info
        
        # Add user input to history
        self.history.append({"role": "user", "content": user_input})
        
        # Base System prompt
        system_prompt = get_system_prompt("hacker")
        
        # Inject tool schemas
        tool_schemas = json.dumps(get_core_tools(), indent=2)
        
        MAX_AUTO_STEPS = 15 
        steps = 0
        
        while steps < MAX_AUTO_STEPS:
            steps += 1
            self.iteration += 1
            
            prompt_content = system_prompt.format(
                previous_findings="\n".join(self.findings) if self.findings else "None",
                current_iteration=self.iteration,
                max_iterations="Unlimited",
                actions_count=len(self.history) // 2,
                failures=0,
                tools=self.dynamic_context.get_tool_arsenal()
            ) 
            
            # Enforce Strict JSON Tool Calling
            prompt_content += f"""\n\n**AVAILABLE TOOLS (JSON SCHEMA):**\n{tool_schemas}
            
**STRICT INSTRUCTIONS:**
You are in an autonomous loop. You MUST respond with a JSON array containing EXACTLY ONE tool call object. Do NOT wrap the JSON in markdown blocks like ```json. Do NOT output any other text before or after the JSON array.
If you need to stop and ask the user for input, or if you have finished the objective, use the `ask_user` tool.

Example format:
[
  {{
    "tool": "execute_command",
    "thought": "I need to run nmap to scan for open ports.",
    "parameters": {{"command": "nmap -p- -sV localhost"}}
  }}
]
"""
            
            recent_history = self.history[-20:] # Keep moderate context window
            
            if not hasattr(self.controller, 'reasoning_llm') or not self.controller.reasoning_llm:
                 self.ui.print_error("No Reasoning LLM available.")
                 return
                 
            with self.ui.loading_indicator("Agent Thinking..."):
                response = self.controller.reasoning_llm.generate(prompt_content, recent_history)
            
            # Attempt to parse strict JSON tool call
            tool_calls = []
            try:
                # Clean up potential markdown or prefix text the LLM might hallucinate
                clean_response = response.strip()
                if clean_response.startswith("```json"): clean_response = clean_response[7:]
                if clean_response.startswith("```"): clean_response = clean_response[3:]
                if clean_response.endswith("```"): clean_response = clean_response[:-3]
                clean_response = clean_response.strip()
                
                # If it's a single object, wrap it in array
                if clean_response.startswith("{") and clean_response.endswith("}"):
                    clean_response = f"[{clean_response}]"
                    
                tool_calls = json.loads(clean_response)
                if not isinstance(tool_calls, list):
                    raise ValueError("Expected a JSON array of tool calls.")
            except Exception as e:
                # LLM failed to follow JSON structure. Fallback to raw conversational dump and ask user.
                self.ui.print_warning(f"Agent failed to format tool call. Raw output:\n{response}")
                self.history.append({"role": "assistant", "content": response})
                self.history.append({"role": "user", "content": "SYSTEM ERROR: You did not output a valid JSON tool call array. Please retry using the strict JSON format."})
                continue
            
            if not tool_calls:
                return # Exit loop if empty
                
            self.history.append({"role": "assistant", "content": json.dumps(tool_calls, indent=2)})
            
            for call in tool_calls:
                tool_name = call.get("tool")
                thought = call.get("thought", "")
                params = call.get("parameters", {})
                
                if thought:
                    self.ui.print_panel(thought, title="Agent Thought", style="cyan")
                
                # Check auto-execute config
                auto_exec = self.config.get('auto_execute_commands', False)
                allowed = True
                
                # Tools that require permission check
                if tool_name in ["execute_command", "write_file"]:
                    action_summary = f"Run: {params.get('command')}" if tool_name == "execute_command" else f"Write to: {params.get('filepath')}"
                    self.ui.print_panel(action_summary, title=f"Tool Call: {tool_name}", style="bold green")
                    # Permissions model disabled based on user preference - agent executes autonomously
                
                if not allowed: continue
                
                # Check if it's a dynamic skill first
                if tool_name in self.plugin_loader.loaded_skills:
                    res = self.plugin_loader.execute_skill(tool_name, params)
                    self.history.append({"role": "user", "content": f"SYSTEM TOOL RESULT (skill {tool_name}):\n{res}"})
                    continue
                
                # Execute specific tools
                if tool_name == "ask_user":
                    prompt_text = params.get("prompt", "User input requested:")
                    self.ui.print_panel(prompt_text, title="Agent Message", style="bold magenta")
                    return # Exit autonomous loop, return control to main chat loop
                    
                elif tool_name == "execute_command":
                    cmd = params.get("command", "")
                    timeout = params.get("timeout", 300)
                    with self.ui.loading_indicator(f"Executing: {cmd[:50]}..."):
                        res = self.controller.executor.execute(cmd, timeout=timeout)
                    
                    # Truncate output for LLM context
                    out_truncated = self.truncate_output(res.get('output', ''))
                    
                    # UI display - masked to reduce clutter (extent/unextent style)
                    if res.get('returncode') == 0:
                        self.ui.print_success(f"Command executed successfully: `{cmd}`")
                    else:
                        self.ui.print_error(f"Command failed (exit {res.get('returncode')}): `{cmd}`")
                        # Show a small snippet if it failed to help user see what went wrong
                        err_snippet = out_truncated[:500] + ("..." if len(out_truncated) > 500 else "")
                        self.ui.print_panel(f"```text\n{err_snippet}\n```", title="Error Output Snippet", style="red")
                    
                    self.history.append({
                        "role": "user",
                        "content": f"SYSTEM TOOL RESULT (execute_command):\nExit Code: {res.get('returncode')}\nOutput:\n{out_truncated}"
                    })
                    self.findings.append(f"Ran `{cmd}`")

                elif tool_name == "todo":
                    action = params.get("action")
                    item = params.get("item", "")
                    if action == "add":
                        self.todos.append(item)
                        result = f"Added '{item}' to todo list."
                    elif action == "remove":
                        if item in self.todos:
                            self.todos.remove(item)
                            result = f"Removed '{item}' from todo list."
                        else:
                            result = f"Item '{item}' not found in todo list."
                    elif action == "clear":
                        self.todos.clear()
                        result = "Cleared todo list."
                    else: # list
                        result = "Current TODOs:\n" + "\n".join([f"- {t}" for t in self.todos]) if self.todos else "Todo list is empty."
                    
                    self.ui.print_panel(result, title="Agent To-Do List", style="yellow")
                    self.history.append({"role": "user", "content": f"SYSTEM TOOL RESULT (todo):\n{result}"})
                    
                elif tool_name == "read_file":
                    filepath = params.get("filepath", "")
                    try:
                        with open(filepath, "r", encoding="utf-8") as f:
                            content = f.read()
                        trunc_content = self.truncate_output(content)
                        self.history.append({"role": "user", "content": f"SYSTEM TOOL RESULT (read_file {filepath}):\n{trunc_content}"})
                    except Exception as e:
                        self.history.append({"role": "user", "content": f"SYSTEM TOOL RESULT (read_file): Error reading {filepath}: {str(e)}"})
                        
                elif tool_name == "write_file":
                    filepath = params.get("filepath", "")
                    content = params.get("content", "")
                    try:
                        # Ensure dir exists
                        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
                        with open(filepath, "w", encoding="utf-8") as f:
                            f.write(content)
                        self.history.append({"role": "user", "content": f"SYSTEM TOOL RESULT (write_file): Successfully wrote to {filepath}"})
                    except Exception as e:
                        self.history.append({"role": "user", "content": f"SYSTEM TOOL RESULT (write_file): Error writing to {filepath}: {str(e)}"})
                        
                elif tool_name == "web_search":
                    from bugpilot.tools.web_search import perform_web_search
                    query = params.get("query", "")
                    result = perform_web_search(query)
                    self.history.append({"role": "user", "content": f"SYSTEM TOOL RESULT (web_search {query}):\n{result}"})
                    
                elif tool_name == "read_url":
                    from bugpilot.tools.web_search import read_url_text
                    url = params.get("url", "")
                    result = read_url_text(url)
                    self.history.append({"role": "user", "content": f"SYSTEM TOOL RESULT (read_url {url}):\n{result}"})
                
                elif tool_name == "cve_search":
                    q = params.get("query", "")
                    out = search_cve(q)
                    self.history.append({"role": "user", "content": f"SYSTEM TOOL RESULT (cve_search):\n{out}"})
                    
                elif tool_name == "owasp_info":
                    cat = params.get("category", "")
                    out = get_owasp_info(cat)
                    self.history.append({"role": "user", "content": f"SYSTEM TOOL RESULT (owasp_info):\n{out}"})
                    
                else:
                    self.history.append({"role": "user", "content": f"SYSTEM ERROR: Unknown tool '{tool_name}'."})

