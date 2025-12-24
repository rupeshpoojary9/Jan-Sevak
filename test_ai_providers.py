import os
import unittest
from unittest.mock import patch
from complaints.ai_service import get_provider, GeminiProvider, GrokProvider

class TestAIProviderSwitching(unittest.TestCase):
    @patch.dict(os.environ, {"AI_PROVIDER": "gemini"})
    def test_gemini_provider_selection(self):
        provider = get_provider()
        self.assertIsInstance(provider, GeminiProvider)
        print("✅ AI_PROVIDER='gemini' -> GeminiProvider selected")

    @patch.dict(os.environ, {"AI_PROVIDER": "grok"})
    def test_grok_provider_selection(self):
        provider = get_provider()
        self.assertIsInstance(provider, GrokProvider)
        print("✅ AI_PROVIDER='grok' -> GrokProvider selected")

    @patch.dict(os.environ, {}, clear=True)
    def test_default_provider_selection(self):
        # Should default to Gemini if not set
        provider = get_provider()
        self.assertIsInstance(provider, GeminiProvider)
        print("✅ AI_PROVIDER missing -> Default (GeminiProvider) selected")

if __name__ == "__main__":
    unittest.main()
