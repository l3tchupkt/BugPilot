import unittest
from bugpilot.agent.tools_schema import get_core_tools

class TestToolsSchema(unittest.TestCase):
    def test_get_core_tools_structure(self):
        tools = get_core_tools()
        self.assertIsInstance(tools, list)
        self.assertGreater(len(tools), 0)
        
        tool_names = [tool['name'] for tool in tools]
        self.assertIn("execute_command", tool_names)
        self.assertIn("read_file", tool_names)
        self.assertIn("write_file", tool_names)
        self.assertIn("cve_search", tool_names)
        
        for tool in tools:
            self.assertIn("name", tool)
            self.assertIn("description", tool)
            self.assertIn("parameters", tool)
            self.assertEqual(tool["parameters"]["type"], "object")

if __name__ == '__main__':
    unittest.main()
