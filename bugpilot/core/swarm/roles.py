import os
import yaml
from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class AgentRole:
    name: str
    description: str
    system_prompt: str
    tools: List[str]
    model_override: Optional[str] = None

class RoleManager:
    """Manages built-in and custom agent roles for the Swarm architecture."""
    
    DEFAULT_ROLES = [
        AgentRole(
            name="recon",
            description="Focuses on mapping the attack surface using active enumeration.",
            system_prompt="You are a Reconnaissance Agent. Your only goal is to map the attack surface. Use tools like nmap, dirb, or curl to gather raw data about the target. Do not attempt exploitation.",
            tools=["execute_command", "read_file"]
        ),
        AgentRole(
            name="researcher",
            description="Finds exploits, documentation, and intelligence.",
            system_prompt="You are a Researcher Agent. Use web search and CVE lookup tools to find intelligence, exploit PoCs, and documentation for the orchestrator.",
            tools=["web_search", "read_url", "cve_search", "owasp_info"]
        ),
        AgentRole(
            name="auditor",
            description="Specialized in Static Application Security Testing (SAST).",
            system_prompt="You are a Code Auditor Agent. You specialize in SAST. Read source code and search for insecure patterns (e.g., hardcoded secrets, SQLi, command injection).",
            tools=["read_file", "execute_command"] # execute_command allows running grep or ripgrep
        ),
        AgentRole(
            name="triager",
            description="Evaluates raw findings, verifies impact, and filters false positives.",
            system_prompt="You are a Bug Bounty Triager. You evaluate raw findings to verify their true impact. Filter out false positives aggressively and assign accurate CVSS severities.",
            tools=["read_file", "ask_user"]
        ),
        AgentRole(
            name="validator",
            description="Actively proves a finding is real (e.g., executing a harmless PoC).",
            system_prompt="You are a Validator Agent. Your job is to take a theoretical finding and actively prove it exists by running harmless verification commands (e.g. curl to check for SSRF or blind XSS callbacks).",
            tools=["execute_command", "read_file"]
        ),
        AgentRole(
            name="exploiter",
            description="Generates and executes payloads based on validated findings.",
            system_prompt="You are an Exploiter Agent. Your job is to take a confirmed vulnerability and generate a working payload or exploit script to gain further access.",
            tools=["execute_command", "write_file", "read_file"]
        ),
        AgentRole(
            name="reporter",
            description="Formats findings into a final markdown report.",
            system_prompt="You are a Reporter Agent. Read the SQLite findings and format them into a highly professional, well-structured markdown report suitable for a client.",
            tools=["read_file", "write_file"]
        )
    ]
    
    def __init__(self):
        self.roles = {role.name: role for role in self.DEFAULT_ROLES}
        self._load_custom_roles()
        
    def _load_custom_roles(self):
        agents_yaml = Path.home() / ".bugpilot" / "agents.yaml"
        if not agents_yaml.exists():
            # Create template
            agents_yaml.parent.mkdir(parents=True, exist_ok=True)
            with open(agents_yaml, "w") as f:
                f.write("""# Define custom Swarm Sub-Agents here
# agents:
#   - name: "sql_ninja"
#     description: "Expert in SQL injection"
#     model: "groq:llama-3.3-70b-versatile"
#     system_prompt: "You are an SQLi expert..."
#     tools: ["execute_command", "read_file"]
""")
            return
            
        try:
            with open(agents_yaml, "r") as f:
                config = yaml.safe_load(f)
                if config and "agents" in config:
                    for agent_data in config["agents"]:
                        role = AgentRole(
                            name=agent_data.get("name", "custom_agent"),
                            description=agent_data.get("description", ""),
                            system_prompt=agent_data.get("system_prompt", "You are a custom agent."),
                            tools=agent_data.get("tools", []),
                            model_override=agent_data.get("model")
                        )
                        self.roles[role.name] = role
        except Exception as e:
            print(f"Error loading custom agents: {e}")
            
    def get_role(self, name: str) -> Optional[AgentRole]:
        return self.roles.get(name.lower())
    
    def get_all_roles(self) -> List[AgentRole]:
        return list(self.roles.values())
