import unittest
from unittest.mock import patch, MagicMock
from bugpilot.tools.web_search import perform_web_search, read_url_text

class TestWebSearch(unittest.TestCase):
    @patch('requests.get')
    def test_perform_web_search(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = '<html><body><a class="result__url" href="http://example.com">Test</a><h2 class="result__title">Test Title</h2><a class="result__snippet">Test Snippet</a></body></html>'
        mock_get.return_value = mock_response
        
        result = perform_web_search("test query")
        self.assertIn("Test Snippet", result)

    @patch('requests.get')
    def test_read_url_text(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = '<html><body><h1>Title</h1><p>Content goes here.</p></body></html>'
        mock_get.return_value = mock_response
        
        result = read_url_text("http://example.com")
        self.assertIn("Title", result)
        self.assertIn("Content goes here.", result)

if __name__ == '__main__':
    unittest.main()
