import unittest
from bugpilot.core.llm.factory import ModelFactory
from bugpilot.core.llm.gemini import GeminiModel
from bugpilot.core.llm.openrouter import OpenRouterModel
from bugpilot.core.llm.deepseek import DeepSeekModel
from bugpilot.core.llm.nvidia import NvidiaModel

class TestLLMFactory(unittest.TestCase):
    def test_factory_creates_correct_models(self):
        # OpenRouter
        model = ModelFactory.create_model("openrouter", api_key="test_key")
        self.assertIsInstance(model, OpenRouterModel)
        
        # DeepSeek
        model = ModelFactory.create_model("deepseek", api_key="test_key")
        self.assertIsInstance(model, DeepSeekModel)
        
        # Nvidia
        model = ModelFactory.create_model("nvidia", api_key="test_key")
        self.assertIsInstance(model, NvidiaModel)
        
    def test_factory_fallback(self):
        # Should fallback to Gemini if unknown provider
        model = ModelFactory.create_model("unknown_provider", api_key="test_key")
        self.assertIsInstance(model, GeminiModel)

if __name__ == '__main__':
    unittest.main()
