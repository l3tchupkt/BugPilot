import os
import sys
import importlib.util
from pathlib import Path

class PluginLoader:
    def __init__(self):
        self.skills_dir = Path.home() / ".bugpilot" / "skills"
        self.loaded_skills = {}
        self.ensure_skills_dir()

    def ensure_skills_dir(self):
        if not self.skills_dir.exists():
            self.skills_dir.mkdir(parents=True, exist_ok=True)
            # Create a sample skill to show users how it works
            sample_skill = self.skills_dir / "sample_skill.py"
            sample_skill.write_text('''
# Sample Bugpilot Skill

TOOL_SCHEMA = {
    "name": "greet_user",
    "description": "A sample skill that returns a greeting.",
    "parameters": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "The name of the user to greet."
            }
        },
        "required": ["name"]
    }
}

def execute(name: str) -> str:
    return f"Hello, {name}! This is a dynamic skill executing."
''')

    def load_all_skills(self) -> dict:
        """Loads all valid skills from the skills directory."""
        if not self.skills_dir.exists():
            return {}

        sys.path.insert(0, str(self.skills_dir))
        
        for file in self.skills_dir.glob("*.py"):
            if file.name.startswith("__"):
                continue
                
            module_name = file.stem
            try:
                spec = importlib.util.spec_from_file_location(module_name, file)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                if hasattr(module, "TOOL_SCHEMA") and hasattr(module, "execute"):
                    schema = module.TOOL_SCHEMA
                    self.loaded_skills[schema["name"]] = {
                        "schema": schema,
                        "execute": module.execute
                    }
            except Exception as e:
                print(f"Failed to load skill {file.name}: {e}")
                
        sys.path.pop(0)
        return self.loaded_skills

    def get_skill_schemas(self) -> list:
        """Return list of schemas to inject into the LLM prompt."""
        return [skill["schema"] for skill in self.loaded_skills.values()]

    def execute_skill(self, name: str, params: dict) -> str:
        """Execute a loaded skill by name."""
        if name in self.loaded_skills:
            try:
                return str(self.loaded_skills[name]["execute"](**params))
            except Exception as e:
                return f"Error executing skill {name}: {str(e)}"
        return f"Skill {name} not found."
