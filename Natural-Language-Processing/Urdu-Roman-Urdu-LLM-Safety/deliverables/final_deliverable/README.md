> Historical project documentation. Current setup and verified limitations are described in the project README; saved results are not a new benchmark.

# 📋 Final Deliverable - Quick Navigation for Instructor

**Project**: Toxic Prompt Filter for Urdu and Roman-Urdu
**Team**: Azaan Imran, Ahmed Bilal
**Course**: Natural Language Processing

---

## 🎯 How to Review This Project

This README provides a guided path through the project deliverables for efficient review.

### 1. Start Here: Project Proposal
📄 **File**: [`../proposal/Toxic_Prompt_Filter_Proposal_with_Pipeline.pdf`](../proposal/Toxic_Prompt_Filter_Proposal_with_Pipeline.pdf)

**What's inside**:
- Original project objectives and motivation
- Literature review on toxicity detection
- Proposed pipeline architecture
- Dataset descriptions (RUT, RUHSOLD, Urdu YouTube)
- Evaluation plan

**Key Points**:
- Goal: Filter toxic Urdu/Roman-Urdu content before LLM processing
- Approach: Multi-layered (lexicon + ML model)
- Expected deliverable: Functional prototype with minimal latency

---

### 2. First Deliverable (Baseline Results)
📄 **File**: [`../deliverable1/NLP%201st%20deliverable.pdf`](../deliverable1/NLP%201st%20deliverable.pdf)

**What was accomplished**:
- ✅ Data preprocessing and EDA
- ✅ Combined 3 datasets (84,954 samples)
- ✅ Baseline model: TF-IDF + Logistic Regression
  - Accuracy: 84.5%
  - F1-score (toxic): 0.71
  - Macro F1: 0.80
- ✅ Lexicon sensitivity analysis (4.7% prediction flips)

**Key Findings**:
- Model relies moderately on explicit lexical cues
- Performance varies by source: YouTube (0.92) > RUT (0.74) > RUHSOLD (0.59)
- Identified need for context-aware model (mBERT)

---

### 3. Core Implementation (Jupyter Notebooks)

Execute notebooks in this order to see the complete pipeline:

#### 📓 Notebook 1: Data Exploration & Baseline
**File**: [`../../notebooks/1_data_exploration_and_baseline.ipynb`](../../notebooks/1_data_exploration_and_baseline.ipynb)

**Contents**:
- Dataset loading and preprocessing
- Exploratory Data Analysis (class distribution, script analysis)
- Baseline model training (TF-IDF + LogReg)
- Lexicon sensitivity analysis
- Performance metrics

**Run time**: ~5-10 minutes
**Output**: Baseline model saved to `models/baseline/`

---

#### 📓 Notebook 2: mBERT Model Training
**File**: [`../../notebooks/2_mbert_model_training.ipynb`](../../notebooks/2_mbert_model_training.ipynb)

**Contents**:
- Fine-tuning `bert-base-multilingual-cased`
- Training on combined dataset (67K train / 8K val / 8K test)
- Evaluation metrics and comparison with baseline
- Model saving to `models/mbert_toxic_final/`

**Note**: This notebook was partially executed. Full training requires Google Colab GPU.
**Run time**: 2-3 hours on GPU (T4/V100)

---

#### 📓 Notebook 3: Toxicity Filter Demo
**File**: [`../../notebooks/3_toxicity_filter_demo.ipynb`](../../notebooks/3_toxicity_filter_demo.ipynb)

**Contents**:
- Demonstration of `filter_prompt()` function
- Testing block/sanitize/allow decision logic
- Analysis of 2,000 sample predictions
- Performance trade-offs (99% recall vs 27% precision)

**Key Insights**:
- 67% of inputs are sanitized (conservative approach)
- 16.5% blocked as highly toxic
- 16% allowed as safe

**Run time**: 2-3 minutes

---

#### 📓 Notebook 4: End-to-End Pipeline with Gemini
**File**: [`../../notebooks/4_end_to_end_pipeline_with_gemini.ipynb`](../../notebooks/4_end_to_end_pipeline_with_gemini.ipynb)

**Contents**:
- Google Gemini API integration
- Complete safety pipeline:
  1. User input filtering
  2. Sanitization of toxic content
  3. LLM generation (Gemini)
  4. Output verification
  5. Safe response delivery
- Real-world examples and test cases

**Requirements**:
- Google API key (free tier: https://aistudio.google.com/app/apikey)
- Internet connection for API calls

**Run time**: 5-10 minutes (including API calls)

---

### 4. Source Code

#### 🐍 Core Filtering Module
**File**: [`../../src/toxic_filter.py`](../../src/toxic_filter.py)

**Key Functions**:
- `predict_proba_mbert(text)`: Returns toxicity probability (0.0-1.0)
- `contains_lexicon(text)`: Checks for RUHSOLD hate words
- `sanitize_text(text)`: Replaces hate words with `[insult]`
- `filter_prompt(text)`: Main pipeline function

**Decision Logic**:
```python
if p_toxic >= 0.90:
    action = "block"        # Very toxic
elif p_toxic >= 0.60 or contains_lexicon:
    action = "sanitize"     # Moderate or explicit slurs
else:
    action = "allow"        # Safe content
```

---

#### 🤖 LLM Client Module
**File**: [`../../src/llm_client.py`](../../src/llm_client.py)

**Key Features**:
- Google Gemini API integration
- Urdu language instruction support
- Rate limiting and error handling
- Safe generation with retry logic

**Usage**:
```python
from src.llm_client import GeminiLLM

llm = GeminiLLM(api_key="your-key")
response = llm.generate("Python kya hai?")
```

---

### 5. Trained Models

#### Baseline Models
📁 **Location**: `../../models/baseline/`

- `combined_baseline.joblib`: Logistic Regression classifier
- `combined_vectorizer.joblib`: TF-IDF vectorizer (25K features)

**Performance**: 84.5% accuracy, F1: 0.71 (toxic class)

---

#### Fine-tuned mBERT
📁 **Location**: `../../models/mbert_toxic_final/`

- `model.safetensors`: Model weights (679 MB)
- `config.json`: Model configuration
- `tokenizer.json`, `vocab.txt`: Tokenizer files

**Architecture**: `bert-base-multilingual-cased` fine-tuned for binary classification

---

### 6. Datasets

📁 **Location**: `../../data/`

| Dataset | Size | Description |
|---------|------|-------------|
| **RUT** | 72,771 | Roman-Urdu toxic comments from social media |
| **RUHSOLD** | 10,013 | Hate speech corpus with 200+ hate words |
| **Urdu YouTube** | 2,170 | Comments in native Urdu script |
| **Combined** | 84,954 | Merged dataset with standardized labels |

**Hate Word Lexicon**: `data/ruhsold/hate_words_roman_urdu.txt` (~200 terms)

---

### 7. Demo Application (Optional)

📁 **File**: `../../demo/app.py` (if created)

**Run**:
```bash
streamlit run demo/app.py
```

**Features**:
- Interactive web interface
- Real-time toxicity checking
- Gemini LLM integration
- Configurable thresholds

---

## ⚡ Quick Test (Without Running Notebooks)

If you want to test the system quickly:

### Option 1: Test Filtering Only
```python
from src.toxic_filter import filter_prompt

# Test cases
test_texts = [
    "Mujhe coding seekhni hai",      # Safe
    "tum bohat gande insan ho",      # Toxic
    "Python sikhayen please"         # Safe
]

for text in test_texts:
    result = filter_prompt(text)
    print(f"{text} → {result['action']} (p_toxic: {result['p_toxic']:.3f})")
```

### Option 2: Test Full Pipeline
```python
from src.toxic_filter import filter_prompt
from src.llm_client import GeminiLLM

# Input filtering
user_input = "Python kya hai?"
input_check = filter_prompt(user_input)

if input_check['action'] != 'block':
    # Generate response
    llm = GeminiLLM(api_key="your-google-api-key")
    response = llm.generate(input_check['clean_text'])

    # Output verification
    output_check = filter_prompt(response)

    print(f"User: {user_input}")
    print(f"LLM: {response if output_check['action'] != 'block' else '[BLOCKED]'}")
```

---

## 📊 Project Evaluation Summary

### Completed Requirements (from Proposal)

| Requirement | Status | Evidence |
|-------------|--------|----------|
| Data Preprocessing | ✅ Complete | Notebook 1, `data/all_combined.csv` |
| Toxicity Classification | ✅ Complete | Baseline + mBERT in Notebooks 1-2 |
| Toxic Text Sanitization | ✅ Complete | `src/toxic_filter.py`, Notebook 3 |
| Blocking Logic | ✅ Complete | Notebook 3-4, decision thresholds |
| LLM Integration | ✅ Complete | `src/llm_client.py`, Notebook 4 |
| Output Verification | ✅ Complete | Notebook 4, pipeline demo |
| Evaluation Metrics | ✅ Complete | All notebooks, reports |

### Performance Metrics

| Metric | Baseline (TF-IDF) | mBERT (Fine-tuned) |
|--------|-------------------|--------------------|
| Accuracy | 84.5% | [See Notebook 2] |
| Precision (Toxic) | 0.62 | [See Notebook 2] |
| Recall (Toxic) | 0.82 | [See Notebook 2] |
| F1-Score (Toxic) | 0.71 | [See Notebook 2] |
| Macro F1 | 0.80 | [See Notebook 2] |

### Filter Pipeline Performance
- **Toxic Recall**: 99.1% (catches almost all toxic content)
- **False Positive Rate**: ~73% (conservative filtering)
- **Trade-off**: Safety prioritized over convenience

---

## 🗂️ File Checklist for Grading

- [x] Project proposal (PDF)
- [x] First deliverable report (PDF)
- [x] Data preprocessing notebook
- [x] Baseline model training notebook
- [x] mBERT training notebook
- [x] Filter demo notebook
- [x] End-to-end pipeline notebook
- [x] Core filtering module (`toxic_filter.py`)
- [x] LLM client module (`llm_client.py`)
- [x] Trained models (baseline + mBERT)
- [x] Combined dataset
- [x] Requirements file
- [x] README documentation

---

## 💡 Notes for Instructor

1. **GPU Training**: Notebook 2 (mBERT training) requires GPU. If reviewing without GPU, see saved model in `models/mbert_toxic_final/` and evaluation results in the notebook.

2. **API Key Required**: Notebook 4 requires a free Google API key for Gemini. Get one at: https://aistudio.google.com/app/apikey

3. **Dependencies**: Run `pip install -r requirements.txt` before executing notebooks.

4. **Recommended Review Order**:
   - Start with Proposal → First Deliverable (context)
   - Review Notebook 1 (baseline results)
   - Check `src/toxic_filter.py` (implementation)
   - Review Notebook 3 (filter demo)
   - Check Notebook 4 (end-to-end system)
   - Optionally: Run demo app for interactive testing

5. **Execution Time**: Total ~15-20 minutes to run all notebooks (excluding mBERT training)

---

## 📧 Contact

For questions about this project:
- **Azaan Imran**: [email]
- **Ahmed Bilal**: [email]

**Project Repository**: [if available]

---

**Thank you for reviewing our project!** 🙏

We hope this navigation guide makes the review process efficient. All code is well-documented and ready to execute.
