import unittest
from unittest.mock import MagicMock, patch
from prompt_toolkit.document import Document
from bugpilot.cli.autocomplete import BugPilotCompleter, get_command_input

class TestAutocomplete(unittest.TestCase):
    def setUp(self):
        self.config_manager = MagicMock()
        self.completer = BugPilotCompleter(config_manager=self.config_manager)

    def test_command_completion(self):
        doc = Document("/he")
        completions = list(self.completer.get_completions(doc, None))
        self.assertTrue(any(c.text == "help" for c in completions))

    def test_theme_completion(self):
        doc = Document("/theme o")
        completions = list(self.completer.get_completions(doc, None))
        self.assertEqual(len(completions), 1)
        self.assertEqual(completions[0].text, "ocean")

    def test_provider_completion(self):
        doc = Document("/model o")
        completions = list(self.completer.get_completions(doc, None))
        providers = [c.text for c in completions]
        self.assertIn("openai", providers)
        self.assertIn("ollama", providers)
        self.assertIn("openrouter", providers)

    @patch('requests.get')
    def test_model_completion_dynamic(self, mock_get):
        # Mock successful API response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": [{"id": "gpt-4-test"}, {"id": "gpt-3.5-test"}]}
        mock_get.return_value = mock_response
        
        self.config_manager.get_api_key.return_value = "sk-test"
        
        doc = Document("/model openai gpt")
        completions = list(self.completer.get_completions(doc, None))
        
        models = [c.text for c in completions]
        self.assertIn("gpt-4-test", models)
        self.assertIn("gpt-3.5-test", models)
        
        # Test caching
        mock_get.reset_mock()
        completions2 = list(self.completer.get_completions(doc, None))
        mock_get.assert_not_called()
        self.assertEqual(len(completions2), len(completions))

    def test_model_completion_fallback(self):
        # Test fallback when no API key
        self.config_manager.get_api_key.return_value = None
        
        doc = Document("/model openai gpt")
        completions = list(self.completer.get_completions(doc, None))
        
        models = [c.text for c in completions]
        self.assertIn("gpt-4o", models)

    @patch('bugpilot.cli.autocomplete.os.path.exists')
    @patch('bugpilot.cli.autocomplete.os.listdir')
    @patch('bugpilot.cli.autocomplete.os.path.isfile')
    def test_file_completion(self, mock_isfile, mock_listdir, mock_exists):
        mock_exists.return_value = True
        mock_listdir.return_value = ["test_file.py", "other.py"]
        mock_isfile.return_value = True
        
        doc = Document("@test")
        completions = list(self.completer.get_completions(doc, None))
        
        files = [c.text for c in completions]
        self.assertIn("test_file.py", files)

if __name__ == '__main__':
    unittest.main()
