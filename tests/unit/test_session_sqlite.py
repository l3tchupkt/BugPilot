import unittest
import os
import sqlite3
import shutil
from pathlib import Path
from unittest.mock import MagicMock
from bugpilot.core.state.session import SessionManager

class TestSessionManager(unittest.TestCase):
    def setUp(self):
        self.test_db_dir = Path("tests/unit/test_db")
        self.test_db_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.test_db_dir / "bugpilot.db"
        
        # Mock config with persistence enabled
        self.mock_config = MagicMock()
        self.mock_config.session.enable_persistence = True
        
    def tearDown(self):
        if self.test_db_dir.exists():
            shutil.rmtree(self.test_db_dir)

    def test_ephemeral_session(self):
        mock_config = MagicMock()
        mock_config.session.enable_persistence = False
        manager = SessionManager(config=mock_config)
        
        session = manager.create_session("Test Objective")
        self.assertEqual(session["objective"], "Test Objective")
        self.assertEqual(session["status"], "active")
        
        manager.add_history("user", "Hello")
        # In ephemeral mode, history is not saved to DB, so we just verify it doesn't crash
        
        manager.add_iteration("thought", {"command": "ls"}, {"success": True}, "analysis")
        self.assertEqual(len(manager.current_session["iterations"]), 1)

    def test_persistent_session(self):
        manager = SessionManager(config=self.mock_config)
        manager.db_path = self.db_path
        manager._init_db()
        
        session = manager.create_session("Persistent Objective")
        
        # Check DB
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT objective FROM sessions WHERE id=?", (session["id"],))
        result = c.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[0], "Persistent Objective")
        
        # Test finding addition
        manager.add_finding({"vulnerability": "SQLi", "severity": "High"})
        c.execute("SELECT finding_json FROM findings WHERE session_id=?", (session["id"],))
        finding = c.fetchone()
        self.assertIsNotNone(finding)
        self.assertIn("SQLi", finding[0])
        conn.close()

if __name__ == '__main__':
    unittest.main()
