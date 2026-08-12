import unittest
import os
import shutil
from pathlib import Path
from bugpilot.core.plugin_loader import PluginLoader

class TestPluginLoader(unittest.TestCase):
    def setUp(self):
        # Override the skills directory to a temporary test directory
        self.test_skills_dir = Path("tests/unit/test_skills")
        self.test_skills_dir.mkdir(parents=True, exist_ok=True)
        
        # Write a mock skill
        mock_skill = self.test_skills_dir / "mock_skill.py"
        mock_skill.write_text('''
TOOL_SCHEMA = {
    "name": "mock_skill",
    "description": "Mock description",
    "parameters": {"type": "object", "properties": {}}
}
def execute(**kwargs):
    return "Mock execution success"
''')

        # We must monkeypatch PluginLoader's init for the test
        self.original_home = Path.home
        Path.home = lambda: Path("tests/unit/test_home")
        
    def tearDown(self):
        Path.home = self.original_home
        if Path("tests/unit/test_home").exists():
            shutil.rmtree("tests/unit/test_home")
        if self.test_skills_dir.exists():
            shutil.rmtree(self.test_skills_dir)

    def test_plugin_loader_initializes_and_loads(self):
        # We need to manually set skills dir for testing because home patching might be too late
        loader = PluginLoader()
        loader.skills_dir = self.test_skills_dir
        
        skills = loader.load_all_skills()
        self.assertIn("mock_skill", skills)
        self.assertEqual(skills["mock_skill"]["schema"]["name"], "mock_skill")
        
        schemas = loader.get_skill_schemas()
        self.assertEqual(len(schemas), 1)
        self.assertEqual(schemas[0]["name"], "mock_skill")
        
        result = loader.execute_skill("mock_skill", {})
        self.assertEqual(result, "Mock execution success")

if __name__ == '__main__':
    unittest.main()
