"""Executor - Runs commands and tools"""

import subprocess
import os
import platform
import threading
import time
from typing import Dict, Any


class Executor:
    """Executes commands safely"""
    
    def __init__(self, safety_config, timeout=300):
        self.safety = safety_config
        self.timeout = timeout
        self.os_type = platform.system().lower()
        if self.os_type == "linux" and "TERMUX_VERSION" in os.environ:
            self.os_type = "termux"
            
        # Background job tracking
        self.jobs = {}
        self.job_counter = 0
        self.lock = threading.Lock()
        
    def check_jobs(self) -> list:
        """Returns and clears finished background jobs"""
        finished = []
        with self.lock:
            for job_id, job in list(self.jobs.items()):
                if job.get('status') == 'finished':
                    finished.append(job)
                    del self.jobs[job_id]
        return finished
        
    def wait_for_job(self, job_id: int) -> dict:
        """Wait for a background job to finish and return result"""
        import time
        while True:
            with self.lock:
                if job_id not in self.jobs:
                    return {'success': False, 'output': f'Job {job_id} not found or already cleared.', 'returncode': -1}
                if self.jobs[job_id]['status'] == 'finished':
                    job = self.jobs.pop(job_id)
                    return job
            time.sleep(1)

    def _run_bg_job(self, job_id: int, exec_cmd: list, cmd_timeout: int, original_command: str):
        try:
            result = subprocess.run(
                exec_cmd,
                capture_output=True,
                text=True,
                timeout=cmd_timeout
            )
            full_output = ""
            if result.stdout:
                full_output += result.stdout
            if result.stderr:
                full_output += (("\n" if full_output else "") + result.stderr)
            
            with self.lock:
                if job_id in self.jobs:
                    self.jobs[job_id].update({
                        'status': 'finished',
                        'success': result.returncode == 0,
                        'output': full_output,
                        'returncode': result.returncode,
                        'command': original_command
                    })
        except subprocess.TimeoutExpired as e:
            out = e.stdout.decode("utf-8") if isinstance(e.stdout, bytes) else e.stdout or ""
            with self.lock:
                if job_id in self.jobs:
                    self.jobs[job_id].update({
                        'status': 'finished',
                        'success': False,
                        'output': f"Execution timed out after {cmd_timeout} seconds.\nPartial Output:\n{out}",
                        'returncode': -1,
                        'command': original_command
                    })
        except Exception as e:
            with self.lock:
                if job_id in self.jobs:
                    self.jobs[job_id].update({
                        'status': 'finished',
                        'success': False,
                        'output': f"Error executing command: {str(e)}",
                        'returncode': -1,
                        'command': original_command
                    })
    
    def execute(self, command: str, timeout: int = None, background: bool = False) -> Dict:
        """Execute shell command"""
        
        # Use provided timeout or default
        cmd_timeout = timeout if timeout else self.timeout
        
        # Safety check
        if any(dangerous in command.lower() for dangerous in self.safety.dangerous_commands):
            return {
                'success': False,
                'output': 'Command blocked by safety rules',
                'blocked': True
            }
        
        try:
            # Prepare cross-platform command execution
            if self.os_type == 'windows':
                # Windows uses powershell for complex commands often used in pentesting
                exec_cmd = ['powershell', '-Command', command]
            elif self.os_type == 'termux':
                # Termux environment
                exec_cmd = ['bash', '-c', f'source ~/.bashrc 2>/dev/null; {command}']
            else:
                # Standard Linux/macOS
                exec_cmd = ['bash', '-c', command]
                
            if background:
                with self.lock:
                    self.job_counter += 1
                    job_id = self.job_counter
                    self.jobs[job_id] = {
                        'job_id': job_id,
                        'command': command,
                        'status': 'running'
                    }
                t = threading.Thread(target=self._run_bg_job, args=(job_id, exec_cmd, cmd_timeout, command), daemon=True)
                t.start()
                return {
                    'success': True,
                    'output': f'Command started in background. Job ID: {job_id}',
                    'job_id': job_id,
                    'returncode': 0,
                    'background': True
                }
                
            # Execute with standard capture
            result = subprocess.run(
                exec_cmd,
                capture_output=True,
                text=True,
                timeout=cmd_timeout
            )
            
            # Combine stdout and stderr for simple logging, but keep them accessible if needed later
            full_output = ""
            if result.stdout:
                full_output += result.stdout
            if result.stderr:
                full_output += (("\n" if full_output else "") + result.stderr)
                
            return {
                'success': result.returncode == 0,
                'output': full_output,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode,
                'timeout_occurred': False
            }
            
        except subprocess.TimeoutExpired as e:
            return {
                'success': False,
                'output': f'Execution timed out after {cmd_timeout} seconds.\nPartial Output:\n{e.stdout.decode("utf-8") if isinstance(e.stdout, bytes) else e.stdout or ""}',
                'returncode': -1,
                'timeout_occurred': True
            }
        except Exception as e:
            return {
                'success': False, 
                'output': f'Error executing command: {str(e)}',
                'returncode': -1,
                'timeout_occurred': False
            }
