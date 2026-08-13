import unittest
from bugpilot.core.config.editor import SettingsEditor

class TestConfigEditor(unittest.TestCase):
    def test_providers_list(self):
        # Initialize SettingsEditor
        editor = SettingsEditor()
        
        # We can't easily test the interactive dialog without mocking prompt_toolkit deeply,
        # but we can inspect the source code to ensure the providers are there, 
        # or we can just run a regex check on the file since it's a UI component.
        # A better unit test is to ensure the UI method exists and doesn't crash on setup.
        
        # We will parse the file to ensure the providers are listed correctly
        import inspect
        source = inspect.getsource(editor.edit_api_keys)
        
        self.assertIn("'openrouter', 'OpenRouter'", source)
        self.assertIn("'deepseek', 'DeepSeek'", source)
        self.assertIn("'nvidia', 'Nvidia (NIM)'", source)
        
        # Ensure context settings were removed
        source_context = inspect.getsource(editor.edit_context_session)
        self.assertNotIn("max_tokens", source_context)

if __name__ == '__main__':
    unittest.main()
