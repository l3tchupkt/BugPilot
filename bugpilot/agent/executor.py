"""Executor - Runs commands and tools"""

import subprocess
import os
import platform
from typing import Dict


class Executor:
    """Executes commands safely"""
    
    def __init__(self, safety_config, timeout=300):
        self.safety = safety_config
        self.timeout = timeout
        self.os_type = platform.system().lower()
        if self.os_type == "linux" and "TERMUX_VERSION" in os.environ:
            self.os_type = "termux"
    
    def execute(self, command: str, timeout: int = None) -> Dict:
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
