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
        
    @patch('bugpilot.agent.executor.threading.Thread')
    def test_execute_background(self, mock_thread):
        executor = Executor(safety_config=self.safety_config)
        executor.os_type = "linux"
        result = executor.execute("sleep 10", background=True)
        
        self.assertTrue(result['success'])
        self.assertTrue(result['background'])
        self.assertEqual(result['job_id'], 1)
        self.assertEqual(len(executor.jobs), 1)
        mock_thread.assert_called_once()
        mock_thread.return_value.start.assert_called_once()
        
    def test_check_jobs(self):
        executor = Executor(safety_config=self.safety_config)
        
        # Add a running job
        executor.jobs[1] = {'job_id': 1, 'status': 'running'}
        # Add a finished job
        executor.jobs[2] = {'job_id': 2, 'status': 'finished', 'output': 'test'}
        
        finished = executor.check_jobs()
        
        self.assertEqual(len(finished), 1)
        self.assertEqual(finished[0]['job_id'], 2)
        self.assertIn(1, executor.jobs)
        self.assertNotIn(2, executor.jobs)
        
    @patch('bugpilot.agent.executor.time.sleep')
    def test_wait_for_job(self, mock_sleep):
        import time
        executor = Executor(safety_config=self.safety_config)
        
        # Mocking time.sleep to simulate state change during the loop
        def mock_sleep_side_effect(*args):
             executor.jobs[1]['status'] = 'finished'
             executor.jobs[1]['output'] = 'done'
             
        mock_sleep.side_effect = mock_sleep_side_effect
        
        executor.jobs[1] = {'job_id': 1, 'status': 'running'}
        result = executor.wait_for_job(1)
        
        self.assertEqual(result['output'], 'done')
        self.assertNotIn(1, executor.jobs)
        mock_sleep.assert_called_once()

if __name__ == '__main__':
    unittest.main()
