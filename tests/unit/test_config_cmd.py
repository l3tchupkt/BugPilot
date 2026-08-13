import unittest
from unittest.mock import MagicMock
from bugpilot.cli.handlers import CommandHandler

class TestConfigCmd(unittest.TestCase):
    def setUp(self):
        self.mock_cli = MagicMock()
        self.mock_cli.config_manager = MagicMock()
        self.mock_cli.config_manager.config = {
            'llm': {'default_provider': 'gemini'},
            'ui': {'theme': 'ocean'}
        }
        self.handler = CommandHandler(self.mock_cli)

    def test_config_set(self):
        self.handler.cmd_config(['set', 'llm.default_provider', 'openai'])
        
        self.assertEqual(self.mock_cli.config_manager.config['llm']['default_provider'], 'openai')
        self.mock_cli.config_manager.save_config.assert_called_once()
        self.mock_cli.ui.print_success.assert_called_with("Updated llm.default_provider to openai")

    def test_config_get(self):
        self.handler.cmd_config(['get', 'ui.theme'])
        self.mock_cli.ui.print_success.assert_called_with("ui.theme = ocean")

if __name__ == '__main__':
    unittest.main()
