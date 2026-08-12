import unittest
from bugpilot.tools.manager import ToolManager

class TestToolManager(unittest.TestCase):
    def setUp(self):
        # Initialize ToolManager but skip the slow check_all_tools by patching it
        with unittest.mock.patch.object(ToolManager, 'check_all_tools', return_value=None):
            self.manager = ToolManager()
            # Manually mock some installed tools for testing
            self.manager.installed_tools = {
                "nmap": True,
                "sqlmap": False,
                "ffuf": True
            }
            
    def test_suggest_tools_for_task(self):
        # Network scan task
        suggestions = self.manager.suggest_tools_for_task("Can you scan the network for open ports?")
        self.assertIn("nmap", suggestions)
        self.assertIn("masscan", suggestions)
        
        # Web fuzzing task
        suggestions = self.manager.suggest_tools_for_task("fuzz the web directory")
        self.assertIn("ffuf", suggestions)
        self.assertIn("gobuster", suggestions)
        
        # SQL injection task
        suggestions = self.manager.suggest_tools_for_task("Find sql injection vulnerabilities")
        self.assertIn("sqlmap", suggestions)
        
    def test_get_missing_tools(self):
        missing = self.manager.get_missing_tools()
        self.assertIn("sqlmap", missing)
        self.assertNotIn("nmap", missing)
        
    def test_get_installed_tools(self):
        installed = self.manager.get_installed_tools()
        self.assertIn("nmap", installed)
        self.assertIn("ffuf", installed)
        self.assertNotIn("sqlmap", installed)

if __name__ == '__main__':
    unittest.main()
