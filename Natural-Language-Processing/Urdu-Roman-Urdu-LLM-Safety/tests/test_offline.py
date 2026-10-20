"""Decision/configuration tests with mocked inference; not a quality benchmark."""
import importlib.util
import os
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import MagicMock, patch

ROOT = Path(__file__).resolve().parents[1]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class OfflinePipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        lexicon = Path(cls.temp.name) / 'lexicon.txt'
        lexicon.write_text('sampleabuse\n', encoding='utf-8')
        transformers = types.SimpleNamespace(
            AutoTokenizer=MagicMock(), AutoModelForSequenceClassification=MagicMock())
        with patch.dict(os.environ, {'TOXIC_LEXICON_PATH': str(lexicon)}), \
             patch.dict(sys.modules, {'transformers': transformers}):
            cls.pipeline = load_module('offline_pipeline', ROOT / 'src/toxic_filter.py')

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def decision(self, text, score, **kwargs):
        with patch.object(self.pipeline, 'predict_proba_mbert', return_value=score):
            return self.pipeline.filter_prompt(text, extract_words=False, **kwargs)

    def test_allow_below_threshold(self):
        result = self.decision('Python programming', 0.1)
        self.assertEqual(result['action'], 'allow')
        self.assertEqual(result['clean_text'], 'Python programming')

    def test_block_boundary(self):
        result = self.decision('example', 0.9, block_threshold=0.9)
        self.assertEqual(result['action'], 'block')
        self.assertEqual(result['clean_text'], '')

    def test_sanitize_boundary(self):
        self.assertEqual(self.decision('example', 0.6, sanitize_threshold=0.6)['action'], 'sanitize')

    def test_lexicon_can_trigger_sanitization(self):
        result = self.decision('you sampleabuse', 0.1)
        self.assertEqual(result['action'], 'sanitize')
        self.assertNotIn('sampleabuse', result['clean_text'])

    def test_script_detection(self):
        self.assertTrue(self.pipeline.detect_urdu_script('اردو'))
        self.assertFalse(self.pipeline.detect_urdu_script('Roman Urdu'))

    def test_mask_respects_word_boundaries(self):
        self.assertEqual(self.pipeline.mask_word('word wordplay WORD', 'word'), 'wordplay')


class GeminiConfigurationTests(unittest.TestCase):
    def setUp(self):
        sys.path.insert(0, str(ROOT))
        from src.llm_client import GeminiLLM
        self.client = GeminiLLM

    def tearDown(self):
        sys.path.remove(str(ROOT))

    def test_missing_key_is_rejected(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(ValueError, 'API key required'):
                self.client()

    def test_environment_model_and_key(self):
        with patch.dict(os.environ, {'GOOGLE_API_KEY': 'unit-test-placeholder', 'GEMINI_MODEL': 'test-model'}), \
             patch('src.llm_client.genai.configure') as configure, \
             patch('src.llm_client.genai.GenerativeModel') as model:
            self.client()
            configure.assert_called_once_with(api_key='unit-test-placeholder')
            model.assert_called_once_with('test-model')


if __name__ == '__main__':
    unittest.main()
