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

    def test_context_truncation(self):
        # Simulate a very long history
        long_message = "A" * 40000  # 40k chars = ~10k tokens
        self.hacker.history = [
            {"role": "system", "content": "system prompt"},
            {"role": "user", "content": "initial request"},
            {"role": "assistant", "content": long_message},
            {"role": "user", "content": long_message},
            {"role": "assistant", "content": long_message},
            {"role": "user", "content": "current request"}
        ]
        
        self.mock_controller.executor.check_jobs.return_value = []
        self.mock_controller.reasoning_llm.generate.return_value = json.dumps([{"tool": "ask_user", "parameters": {"prompt": "done"}}])
        
        self.hacker.chat("trigger loop")
        
        # Original length was 6, plus the new "trigger loop", plus the "ask_user" response = 8
        # However, it should have been trimmed to stay under 32k tokens. 
        # Total tokens before loop: ~30k tokens. Wait, 40000 chars * 3 = 120,000 chars = 30k tokens.
        # Let's add more to trigger the >32k threshold.
        self.hacker.history.insert(2, {"role": "assistant", "content": long_message})
        # Now it's 4 * 10k tokens = 40k tokens. It should trim.
        
        self.hacker.chat("trigger loop 2")
        
        # Verify the system prompt and initial request are still there
        self.assertEqual(self.hacker.history[0]["role"], "system")
        self.assertEqual(self.hacker.history[1]["role"], "user")
        self.assertEqual(self.hacker.history[1]["content"], "initial request")
        
        # Verify total tokens is < 32000
        current_tokens = sum(len(msg['content']) // 4 for msg in self.hacker.history)
        self.assertLessEqual(current_tokens, 32000)

    def test_background_job_notification(self):
        # Mock executor returning a finished job
        self.mock_controller.executor.check_jobs.return_value = [{
            'job_id': 1,
            'command': 'sleep 10',
            'returncode': 0,
            'output': 'done sleeping'
        }]
        self.mock_controller.reasoning_llm.generate.return_value = json.dumps([{"tool": "ask_user", "parameters": {"prompt": "done"}}])
        
        self.hacker.chat("check background")
        
        # Verify job notification was injected before the assistant response
        system_event = [msg for msg in self.hacker.history if "SYSTEM EVENT: Background Job 1" in msg.get("content", "")]
        self.assertEqual(len(system_event), 1)
        self.assertIn("done sleeping", system_event[0]["content"])
        
    def test_wait_for_job_tool(self):
        # Mock wait_for_job tool call
        mock_response = json.dumps([{
            "tool": "wait_for_job",
            "parameters": {"job_id": 99}
        }])
        
        self.mock_controller.executor.check_jobs.return_value = []
        self.mock_controller.executor.wait_for_job.return_value = {
            'returncode': 0,
            'output': 'job 99 done'
        }
        
        def mock_generate(*args, **kwargs):
            if "job 99 done" not in str(self.hacker.history):
                return mock_response
            return json.dumps([{"tool": "ask_user", "parameters": {"prompt": "done"}}])
            
        self.mock_controller.reasoning_llm.generate.side_effect = mock_generate
        
        self.hacker.chat("wait for it")
        
        self.mock_controller.executor.wait_for_job.assert_called_once_with(99)
        wait_result = [msg for msg in self.hacker.history if "SYSTEM TOOL RESULT (wait_for_job 99)" in msg.get("content", "")]
        self.assertEqual(len(wait_result), 1)
        self.assertIn("job 99 done", wait_result[0]["content"])

if __name__ == '__main__':
    unittest.main()
