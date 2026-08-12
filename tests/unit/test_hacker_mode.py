import unittest
from unittest.mock import MagicMock, patch
import json
from bugpilot.modes.hacker import HackerMode

class TestHackerMode(unittest.TestCase):
    def setUp(self):
        self.mock_controller = MagicMock()
        self.mock_ui = MagicMock()
        self.mock_config = MagicMock()
        self.mock_config.get.return_value = False
        
        self.hacker = HackerMode(self.mock_controller, self.mock_ui, self.mock_config)

    def test_todo_tool(self):
        # Simulate LLM returning a tool call to add a todo
        mock_response = json.dumps([{
            "tool": "todo",
            "parameters": {"action": "add", "item": "Test Task"}
        }])
        
        self.mock_controller.reasoning_llm.generate.return_value = mock_response
        
        # We need to break the autonomous loop after 1 iteration, so we mock ask_user after the first
        def mock_generate(*args, **kwargs):
            if not self.hacker.todos:
                return mock_response
            return json.dumps([{"tool": "ask_user", "parameters": {"prompt": "done"}}])
            
        self.mock_controller.reasoning_llm.generate.side_effect = mock_generate
        
        self.hacker.chat("start")
        self.assertIn("Test Task", self.hacker.todos)

if __name__ == '__main__':
    unittest.main()
