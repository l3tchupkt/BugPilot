import unittest
from unittest.mock import patch, MagicMock
from bugpilot.agent.executor import Executor
from types import SimpleNamespace

class TestExecutor(unittest.TestCase):
    def setUp(self):
        self.safety_config = SimpleNamespace(dangerous_commands=['rm -rf', 'mkfs', 'format'])
        
    def test_safety_check_blocks_dangerous_command(self):
        executor = Executor(safety_config=self.safety_config)
        result = executor.execute("rm -rf /")
        self.assertFalse(result['success'])
        self.assertTrue(result['blocked'])
        self.assertIn("blocked", result['output'])
        
    @patch('bugpilot.agent.executor.subprocess.run')
    def test_execute_success(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout="test output", stderr="")
        executor = Executor(safety_config=self.safety_config)
        executor.os_type = "linux"
        result = executor.execute("echo 'test output'")
        
        self.assertTrue(result['success'])
        self.assertEqual(result['stdout'], "test output")
        self.assertEqual(result['returncode'], 0)
        self.assertFalse(result['timeout_occurred'])
        
    @patch('bugpilot.agent.executor.subprocess.run')
    def test_execute_timeout(self, mock_run):
        import subprocess
        mock_run.side_effect = subprocess.TimeoutExpired(cmd="sleep 10", timeout=1, output=b"partial")
        executor = Executor(safety_config=self.safety_config)
        result = executor.execute("sleep 10", timeout=1)
        
        self.assertFalse(result['success'])
        self.assertTrue(result['timeout_occurred'])
        self.assertIn("timed out", result['output'])
        self.assertEqual(result['returncode'], -1)

if __name__ == '__main__':
    unittest.main()
