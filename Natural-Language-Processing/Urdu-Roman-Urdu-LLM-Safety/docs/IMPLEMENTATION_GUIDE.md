> Historical project documentation. Current setup and verified limitations are described in the project README; saved results are not a new benchmark.

# Implementation Guide

## Architecture Overview

### System Components

1. **Toxicity Detection Engine** (`src/toxic_filter.py`)
   - mBERT-based sentence classification
   - Attention-weighted word attribution
   - Hybrid toxic word identification

2. **LLM Integration** (`src/llm_client.py`)
   - Google Gemini API client
   - Multi-language support (Urdu, Roman Urdu, English)
   - Output safety verification

3. **Web Interface** (`demo/app.py`)
   - Streamlit-based UI
   - Real-time analysis
   - Interactive threshold controls

## Core Algorithms

### Hybrid Toxic Word Identification

Three-method approach for robust word-level detection:

```
For each attention-identified word:
  1. Lexicon Check → Instant identification (O(1))
  2. Individual Scoring → Test word in isolation  
  3. Differential Scoring → Test contribution to sentence toxicity
```

**Example:**
```
Input: "c++ kya kutti aur badtameez cheez hai"
Toxicity: 80.81%

Word Analysis:
  - kutti:     100% (lexicon match)
  - badtameez:  99.6% (individual scoring)
  - kya:        0.1% (filtered - not toxic)
  - cheez:      0.1% (filtered - not toxic)
  - aur:        0.1% (filtered - not toxic)

Output: "c++ kya [insult] aur [insult] cheez hai"
```

### Differential Scoring

Tests if removing a word reduces sentence toxicity:

```python
delta = p_toxic(full_sentence) - p_toxic(sentence_without_word)

if delta >= 0.20:  # 20% threshold
    word_is_toxic = True
```

This eliminates false positives from grammatical words that have high attention but low actual toxicity.

## API Reference

### `filter_prompt(text, **kwargs)`

Main entry point for toxicity filtering.

**Parameters:**
- `text` (str): Input text
- `extract_words` (bool): Extract toxic words (default: True)
- `block_threshold` (float): Block threshold (default: 0.90)
- `sanitize_threshold` (float): Sanitize threshold (default: 0.60)

**Returns:**
```python
{
    'action': 'allow|sanitize|block',
    'p_toxic': 0.0-1.0,
    'original_text': str,
    'clean_text': str,
    'toxic_words': [(word, confidence), ...],
    'has_lexicon': bool
}
```

### `GeminiLLM.generate(prompt, **kwargs)`

Generate LLM response with safety checks.

**Parameters:**
- `prompt` (str): User question
- `language` (str): "roman-urdu"|"urdu"|"english"
- `max_tokens` (int): Maximum response length
- `temperature` (float): Sampling temperature (0.0-1.0)

**Returns:**
- `str`: Generated response text

## Configuration

### Toxicity Thresholds

Located in `src/toxic_filter.py`:

```python
TOXICITY_BLOCK_THRESHOLD = 0.90      # Block if ≥90% toxic
TOXICITY_SANITIZE_THRESHOLD = 0.60   # Sanitize if ≥60% toxic
```

### Differential Scoring Threshold

Located in `src/toxic_filter.py:identify_toxic_words_robust()`:

```python
delta_threshold = 0.20  # Require 20% toxicity reduction
```

Higher values = fewer false positives, may miss subtle toxic words
Lower values = catch more toxic words, may include false positives

## Performance Optimization

### Batch Processing

Use `predict_proba_mbert_batch()` for multiple texts:

```python
texts = ["text1", "text2", "text3"]
toxicities = predict_proba_mbert_batch(texts)
```

**Performance:**
- Single text: ~150ms
- Batch of 10: ~300ms (2x faster than sequential)

### GPU Acceleration

Ensure PyTorch detects CUDA:

```python
import torch
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
```

**Speedup:**
- CPU (Intel i7): ~150ms per text
- GPU (NVIDIA RTX): ~50ms per text (3x faster)

## Testing

### Run Tests

```bash
# Test toxic detection
python tests/test_toxic_detection.py

# Test LLM integration  
python tests/test_llm_integration.py
```

### Expected Output

```
======================================================================
DIFFERENTIAL SCORING TEST - User's Example
======================================================================

Found 2 toxic words:
  • kutti           100.0%  (lexicon)
  • badtameez        99.6%  (individual)

✅ All toxic words identified
✅ No false positives
✅ Toxic words successfully sanitized

🎉 ALL TESTS PASSED!
======================================================================
```

## Deployment

### Production Checklist

- [ ] Model files in `models/mbert_toxic_final/`
- [ ] Lexicon file in `data/lexicons/ruhsold_hate_words.txt`
- [ ] Environment variables set (GOOGLE_API_KEY if using LLM)
- [ ] Tests passing
- [ ] Thresholds configured for your use case

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["streamlit", "run", "demo/app.py", "--server.port=8501"]
```

### Environment Variables

```bash
export GOOGLE_API_KEY="your-api-key"  # For Gemini LLM
```

## Troubleshooting

### Issue: "Model not found"

**Solution:** Ensure `models/mbert_toxic_final/` contains:
- `config.json`
- `pytorch_model.bin`
- `vocab.txt`
- `tokenizer_config.json`

### Issue: "Lexicon not found"

**Solution:** Check path in `src/toxic_filter.py` line 32:
```python
LEXICON_PATH = ROOT / "data" / "lexicons" / "ruhsold_hate_words.txt"
```

### Issue: High false positive rate

**Solution:** Increase `delta_threshold` in `identify_toxic_words_robust()`:
```python
delta_threshold = 0.25  # Stricter filtering
```

### Issue: Missing toxic words

**Solution:** Decrease `delta_threshold`:
```python
delta_threshold = 0.15  # More sensitive
```

## Advanced Usage

### Custom Lexicon

Add words to `data/lexicons/ruhsold_hate_words.txt`:
```
newword1
newword2
```

Reload module to apply changes.

### Custom Model

Train your own mBERT model and place in `models/`:
```python
MODEL_DIR = ROOT / "models" / "your_custom_model"
```

### Multilingual Support

The system auto-detects and handles:
- Roman Urdu (Latin script)
- Urdu Script (Arabic script - auto-transliterated)
- Mixed scripts

## Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new features
4. Ensure all tests pass
5. Submit pull request

## Support

For issues, questions, or feature requests, please open an issue on GitHub.

---

**Last Updated**: December 2025
