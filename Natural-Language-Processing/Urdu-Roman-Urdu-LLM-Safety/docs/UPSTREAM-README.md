> Historical project documentation. Current setup and verified limitations are described in the project README; saved results are not a new benchmark.

# Roman Urdu Toxicity Filter with LLM Integration

A academic demonstration toxicity detection and content moderation system for Roman Urdu text, featuring mBERT-based classification, attention-based word identification, and safe LLM response generation with Google Gemini.

## Features

### Core Capabilities
- **Multilingual Toxicity Detection**: Fine-tuned mBERT model for Roman Urdu/Hindi text classification
- **Intelligent Word-Level Attribution**: Hybrid approach combining lexicon matching, differential scoring, and individual toxicity analysis
- **Automatic Urdu Script Handling**: Detects and transliterates Urdu script to Roman for seamless processing
- **Three-Tier Content Moderation**: ALLOW, SANITIZE, or BLOCK actions based on configurable thresholds
- **LLM Integration**: Safe response generation with Google Gemini, including output toxicity verification

### Technical Highlights
- **Robust False Positive Elimination**: Data-driven differential scoring eliminates grammatical word false positives
- **Batch Processing Optimization**: Efficient parallel processing for word-level toxicity analysis
- **academic demonstration Architecture**: Modular design with clean separation of concerns
- **Real-time Performance**: Optimized for low-latency inference

## Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Basic Usage

```python
from src.toxic_filter import filter_prompt

result = filter_prompt("Python kya hai?")
print(f"Toxicity: {result['p_toxic']:.2%}")
print(f"Action: {result['action']}")
```

### Streamlit Demo

```bash
streamlit run demo/app.py
```

## Project Structure

```
Project/
├── src/
│   ├── toxic_filter.py       # Core toxicity detection engine
│   └── llm_client.py          # Gemini LLM integration
├── demo/
│   └── app.py                 # Streamlit web interface
├── data/
│   └── lexicons/
│       └── ruhsold_hate_words.txt  # 723 hate words lexicon
├── models/
│   └── mbert_toxic_final/     # Fine-tuned mBERT model
├── tests/
│   ├── test_toxic_detection.py
│   └── test_llm_integration.py
└── requirements.txt
```

## Documentation

For detailed documentation, see [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md)

## License

MIT License

---

**Version**: 1.0.0 | **Status**: academic demonstration
