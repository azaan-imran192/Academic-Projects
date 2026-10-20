"""
toxic_filter.py

Core Toxic Prompt Filter pipeline:
- Loads fine-tuned mBERT model
- Loads RUHSOLD hate-word lexicon
- Provides:
    - predict_proba_mbert(text)
    - sanitize_text(text)
    - filter_prompt(text) -> dict with action + cleaned text
"""

import os
from pathlib import Path
import re
import regex as rx
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from collections import defaultdict


os.environ["TRANSFORMERS_NO_TF"] = "1"
os.environ["TRANSFORMERS_NO_FLAX"] = "1"

ROOT = Path(__file__).resolve().parent.parent
MODEL_DIR = Path(os.getenv("TOXIC_MODEL_DIR", str(ROOT / "models" / "mbert_toxic_final")))
LEXICON_PATH = Path(os.getenv("TOXIC_LEXICON_PATH", str(ROOT / "data" / "ruhsold" / "hate_words_roman_urdu.txt")))

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_DIR,
    output_attentions=True
)
model.to(device)
model.eval()


URDU_SCRIPT_PATTERN = re.compile(r'[\u0600-\u06ff\u0750-\u077f\ufb50-\ufdff\ufe70-\ufefc]')

def detect_urdu_script(text: str) -> bool:
    """
    Detect if text contains Urdu script (Perso-Arabic characters).

    Args:
        text: Input string to check

    Returns:
        True if text contains Urdu script characters, False otherwise

    Unicode Ranges for Urdu:
        - U+0600 to U+06FF: Arabic
        - U+0750 to U+077F: Arabic Supplement
        - U+FB50 to U+FDFF: Arabic Presentation Forms-A
        - U+FE70 to U+FEFC: Arabic Presentation Forms-B

    Examples:
        >>> detect_urdu_script("تم سور ہو")
        True
        >>> detect_urdu_script("tum soor ho")
        False
    """
    return bool(URDU_SCRIPT_PATTERN.search(str(text)))



URDU_TO_ROMAN = {
    'ا': 'a',
    'ب': 'b',
    'پ': 'p',
    'ت': 't',
    'ٹ': 't',
    'ث': 's',
    'ج': 'j',
    'چ': 'ch',
    'ح': 'h',
    'خ': 'kh',
    'د': 'd',
    'ڈ': 'd',
    'ذ': 'z',
    'ر': 'r',
    'ڑ': 'r',
    'ز': 'z',
    'ژ': 'zh',
    'س': 's',
    'ش': 'sh',
    'ص': 's',
    'ض': 'z',
    'ط': 't',
    'ظ': 'z',
    'ع': '',
    'غ': 'gh',
    'ف': 'f',
    'ق': 'q',
    'ک': 'k',
    'گ': 'g',
    'ل': 'l',
    'م': 'm',
    'ن': 'n',
    'ں': 'n',
    'و': 'o',
    'ہ': 'h',
    'ھ': 'h',
    'ء': '',
    'ی': 'i',
    'ے': 'e',
    'َ': 'a',
    'ِ': 'i',
    'ُ': 'u',
    'ً': 'an',
    'ٍ': 'in',
    'ٌ': 'un',
    'ّ': '',
    'ْ': '',
}

URDU_WORD_MAPPINGS = {
    'سور': 'soor',
    'سوار': 'suaar',
    'کتے': 'kuttay',
    'کتا': 'kutta',
    'کتی': 'kutti',
    'گندو': 'gandu',
    'گندا': 'ganda',
    'گندے': 'gande',
    'حرامی': 'harami',
    'حرام': 'haram',
    'سالا': 'saala',
    'سالے': 'saale',
    'کمینہ': 'kameena',
    'کمینا': 'kameena',
}

def transliterate_urdu_to_roman(text: str) -> str:
    """
    Transliterate Urdu script text to Roman Urdu.

    Uses word-level mappings for common toxic words, falls back to
    character-level mapping for other words.

    Args:
        text: Urdu script text (e.g., "تم سور ہو")

    Returns:
        Roman Urdu transliteration (e.g., "tum soor ho")

    Examples:
        >>> transliterate_urdu_to_roman("تم سور ہو")
        'tum soor ho'
        >>> transliterate_urdu_to_roman("تم کتے ہو")
        'tum kuttay ho'

    Note:
        This uses a hybrid approach:
        1. Word-level mappings for known toxic words (better accuracy)
        2. Character-level mapping for other words (reasonable approximation)

        More sophisticated libraries like urduhack or ai4bharat-transliteration
        could be used but may have installation issues on some platforms.
    """
    if not detect_urdu_script(text):
        return text

    import re
    words_and_separators = re.findall(r'\S+|\s+', text)

    result = []
    for token in words_and_separators:
        if token.isspace():
            result.append(token)
            continue

        if token in URDU_WORD_MAPPINGS:
            result.append(URDU_WORD_MAPPINGS[token])
        else:
            char_result = []
            for char in token:
                if char in URDU_TO_ROMAN:
                    char_result.append(URDU_TO_ROMAN[char])
                elif char in '.,!?;:()-"\'':
                    char_result.append(char)
                elif char.isdigit():
                    char_result.append(char)
                else:
                    char_result.append(char)

            result.append(''.join(char_result))

    return ''.join(result)



def normalize_roman_urdu(text: str) -> str:
    """
    Normalize Roman Urdu text to handle spelling variations:
    - Reduces repeated characters (ganduuuu -> gandu, kuttay -> kutay)
    - Normalizes common transliteration variations
    - Preserves word boundaries

    This helps match spelling variations in Roman Urdu which has no standard spelling.
    """
    text = text.lower()

    text = re.sub(r'(.)\1{2,}', r'\1\1', text)

    replacements = {
        'ph': 'f',
        'kh': 'k',
        'gh': 'g',
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text


def get_word_stem(word: str) -> str:
    """
    Extract the core 'stem' of a Roman Urdu word by removing common suffixes.
    This helps match variations like: saala, saalay, saale, saali (all have 'saal' stem)

    Common Roman Urdu suffixes: -a, -e, -i, -o, -y, -ay, -an, -on, -un
    """
    word = word.lower().strip()

    suffixes_to_try = ['iyan', 'iyaan', 'aan', 'oon', 'aay', 'eey', 'ay', 'on', 'an', 'un', 'o', 'a', 'e', 'i', 'y']

    for suffix in suffixes_to_try:
        if len(word) > 3 and word.endswith(suffix):
            stem = word[:-len(suffix)]
            if len(stem) >= 3:
                return stem

    return word


def generate_fuzzy_pattern(word: str) -> str:
    """
    Generate a regex pattern that matches spelling variations of a word.
    Handles:
    - Single/double consonants (kutay matches kuttay)
    - Optional repeated vowels (gandu matches ganduuu)
    - Character variations in Roman Urdu
    - Suffix variations (saala, saalay, saale all match)

    Example: 'gandu' -> 'g+a+n+d+u+' (matches gandu, gaandu, ganduuuu)
    """
    word = normalize_roman_urdu(word)

    stem = get_word_stem(word)

    vowels = 'aeiou'

    common_doubled = 'tdnklrs'

    pattern_parts = []
    for char in stem:
        if char in vowels:
            pattern_parts.append(f"{char}{{1,3}}")
        elif char in common_doubled:
            pattern_parts.append(f"{char}{{1,2}}")
        else:
            pattern_parts.append(f"{char}{{1,2}}")

    pattern = ''.join(pattern_parts) + r'[aeiouy]{0,3}'

    return pattern



with open(LEXICON_PATH, encoding="utf-8", errors="ignore") as f:
    HATE_WORDS_RAW = [
        w.strip() for w in f
        if w.strip() and not w.startswith("_")
    ]

hate_words_normalized = {}
for word in HATE_WORDS_RAW:
    normalized = normalize_roman_urdu(word)
    if normalized not in hate_words_normalized:
        hate_words_normalized[normalized] = word

HATE_WORDS = list(hate_words_normalized.keys())

fuzzy_patterns = [generate_fuzzy_pattern(w) for w in HATE_WORDS]

LEXICON_PATTERN = rx.compile(
    r"\b(" + "|".join(fuzzy_patterns) + r")\b",
    flags=rx.IGNORECASE,
)


def contains_lexicon(text: str) -> bool:
    """
    Return True if any hate-word from the lexicon appears in text.
    Uses fuzzy matching to catch spelling variations.
    """
    return bool(LEXICON_PATTERN.search(str(text)))


def sanitize_text(text: str, toxic_words: list = None) -> str:
    """
    Replace toxic words with a neutral placeholder [insult].

    Two-stage sanitization:
    1. Replace differential-scoring-identified toxic words (exact matching) - PRIMARY
    2. Replace RUHSOLD lexicon words (fuzzy matching) - FALLBACK

    With differential scoring, we no longer need SKIP_WORDS list because
    the identification already filters out false positives.

    Args:
        text: Input text to sanitize
        toxic_words: Optional list of (word, confidence) tuples from robust identification

    Returns:
        Sanitized text with toxic words replaced by [insult]

    Examples:
        >>> sanitize_text("tum kuttay ho")
        'tum [insult] ho'  # lexicon match

        >>> sanitize_text("c++ kya kutti aur badtameez cheez hai",
        ...               toxic_words=[("kutti", 1.0), ("badtameez", 0.72)])
        'c++ kya [insult] aur [insult] cheez hai'
        # Only kutti and badtameez replaced, kya/cheez/aur kept (not toxic)
    """
    import re

    sanitized = str(text)

    if toxic_words:
        for word, confidence in toxic_words:
            if len(word) <= 2:
                continue

            pattern = r'\b' + re.escape(word) + r'\b'
            sanitized = re.sub(pattern, '[insult]', sanitized, flags=re.IGNORECASE)

    sanitized = LEXICON_PATTERN.sub("[insult]", sanitized)

    return sanitized



def extract_attention_weights(text: str, max_length: int = 128):
    """
    Extract attention weights from mBERT for toxic word attribution.

    Args:
        text: Input text
        max_length: Maximum sequence length for BERT (default: 128)

    Returns:
        tuple: (tokens, attention_scores, input_ids, logits)
            - tokens: List of WordPiece tokens
            - attention_scores: Aggregated attention per token [seq_len]
            - input_ids: Token IDs
            - logits: Model output logits [2]

    Note:
        mBERT has 12 layers × 12 attention heads.
        Attention shape: [batch=1, heads=12, seq_len, seq_len]
    """
    if detect_urdu_script(text):
        text = transliterate_urdu_to_roman(text)

    enc = tokenizer(
        text,
        padding="max_length",
        truncation=True,
        max_length=max_length,
        return_tensors="pt",
    )
    enc = {k: v.to(device) for k, v in enc.items()}

    with torch.no_grad():
        outputs = model(**enc)

    logits = outputs.logits[0]
    attentions = outputs.attentions
    input_ids = enc['input_ids'][0]
    tokens = tokenizer.convert_ids_to_tokens(input_ids)

    aggregated_attention = aggregate_attention_rollout(attentions)

    return tokens, aggregated_attention, input_ids, logits


def aggregate_attention_rollout(attentions):
    """
    Aggregate attention across all 12 layers using attention rollout.

    Attention Rollout: Multiply attention matrices across layers to capture
    information flow from input to classification token [CLS].

    Args:
        attentions: Tuple of 12 attention tensors
                   Each tensor shape: [batch=1, heads=12, seq_len, seq_len]

    Returns:
        np.ndarray: Attention scores per token [seq_len]
        Represents each token's contribution to [CLS] prediction

    Algorithm:
        1. Average attention across all heads per layer
        2. Add residual connections (I + attention)
        3. Renormalize to make rows sum to 1
        4. Multiply matrices across layers
        5. Extract attention to [CLS] token

    References:
        - "Quantifying Attention Flow in Transformers" (Abnar & Zuidema, 2020)
        - https://arxiv.org/abs/2005.00928
    """
    import numpy as np

    attention_matrix = None

    for layer_attention in attentions:
        avg_attention = layer_attention[0].mean(dim=0)

        seq_len = avg_attention.size(0)
        identity = torch.eye(seq_len).to(avg_attention.device)
        avg_attention = avg_attention + identity

        avg_attention = avg_attention / avg_attention.sum(dim=-1, keepdim=True)

        if attention_matrix is None:
            attention_matrix = avg_attention
        else:
            attention_matrix = torch.matmul(avg_attention, attention_matrix)

    cls_attention = attention_matrix[0, :]

    return cls_attention.cpu().numpy()


def map_tokens_to_words(tokens, attention_scores, input_ids):
    """
    Map WordPiece tokens back to original words with aggregated scores.

    mBERT uses WordPiece tokenization which splits words into subwords:
    - "gandu" → ["gan", "##du"]
    - "kuttay" → ["ku", "##tta", "##y"]

    Args:
        tokens: List of WordPiece tokens (e.g., ["tu", "##m", "gan", "##du"])
        attention_scores: Attention score per token [seq_len]
        input_ids: Token IDs [seq_len]

    Returns:
        List of tuples: [(word, score, token_indices), ...]
        Example: [("tum", 0.15, [1,2]), ("gandu", 0.45, [3,4]), ...]

    Note:
        - Normal tokens: "tum", "gandu"
        - Subword tokens: "##du" (## prefix indicates continuation)
        - Special tokens: [CLS], [SEP], [PAD] (filtered out)
    """
    import numpy as np

    words = []
    current_word = ""
    current_score = 0.0
    current_indices = []

    for i, (token, score) in enumerate(zip(tokens, attention_scores)):
        if token in ['[CLS]', '[SEP]', '[PAD]']:
            continue

        if token.startswith("##"):
            current_word += token[2:]
            current_score += score
            current_indices.append(i)
        else:
            if current_word:
                words.append((
                    current_word,
                    current_score,
                    current_indices.copy()
                ))

            current_word = token
            current_score = score
            current_indices = [i]

    if current_word:
        words.append((current_word, current_score, current_indices))

    return words


def extract_toxic_words(text: str, top_k: int = 5, min_score: float = 0.05):
    """
    Extract words contributing to toxicity using attention attribution.

    Uses attention rollout to identify which words the mBERT model focuses on
    when making toxicity predictions.

    Args:
        text: Input text
        top_k: Return top-k most toxic words (default: 5)
        min_score: Minimum attention score threshold (default: 0.05)

    Returns:
        List of tuples: [(word, contribution_score), ...]
        Sorted by score descending

    Examples:
        >>> extract_toxic_words("tum gandu aur kutti ho")
        [("gandu", 0.42), ("kutti", 0.38), ("tum", 0.12)]

        >>> extract_toxic_words("hello world")
        []  # Not toxic

    Algorithm:
        1. Extract attention weights from mBERT
        2. Map WordPiece tokens to original words
        3. Normalize scores to [0, 1]
        4. Filter by min_score and top_k
        5. Return sorted by contribution
    """
    tokens, attention_scores, input_ids, logits = extract_attention_weights(text)

    probs = torch.softmax(logits, dim=-1)
    p_toxic = probs[1].item()

    if p_toxic < 0.5:
        return []

    words_with_scores = map_tokens_to_words(tokens, attention_scores, input_ids)

    if not words_with_scores:
        return []

    max_score = max(score for _, score, _ in words_with_scores)
    if max_score > 0:
        words_with_scores = [
            (word, score / max_score, indices)
            for word, score, indices in words_with_scores
        ]

    filtered_words = [
        (word, float(score))
        for word, score, _ in words_with_scores
        if score >= min_score
    ]

    filtered_words.sort(key=lambda x: x[1], reverse=True)

    return filtered_words[:top_k]



def predict_proba_mbert_batch(texts: list, max_length: int = 128) -> list:
    """
    Batch process multiple texts for efficient toxicity prediction.

    Args:
        texts: List of input texts
        max_length: Maximum sequence length for BERT (default: 128)

    Returns:
        List of toxicity probabilities (0.0 to 1.0), one per input text

    Examples:
        >>> texts = ["hello", "tum gandu ho", "good morning"]
        >>> predict_proba_mbert_batch(texts)
        [0.02, 0.97, 0.01]
    """
    if not texts:
        return []

    texts_processed = [
        transliterate_urdu_to_roman(text) if detect_urdu_script(text) else text
        for text in texts
    ]

    encodings = tokenizer(
        texts_processed,
        padding=True,
        truncation=True,
        max_length=max_length,
        return_tensors="pt"
    )
    encodings = {k: v.to(device) for k, v in encodings.items()}

    with torch.no_grad():
        outputs = model(**encodings)
        probs = torch.softmax(outputs.logits, dim=-1)
        p_toxics = probs[:, 1].cpu().tolist()

    return [float(p) for p in p_toxics]


def predict_proba_mbert(text: str, max_length: int = 128) -> float:
    """
    Return P(toxic=1) from the fine-tuned mBERT model for a single string.

    Automatically detects and transliterates Urdu script to Roman Urdu before processing.

    Args:
        text: Input text (Roman Urdu or Urdu script)
        max_length: Maximum sequence length for BERT (default: 128)

    Returns:
        Probability of toxicity (0.0 to 1.0)

    Examples:
        >>> predict_proba_mbert("tum gandu ho")
        0.971
        >>> predict_proba_mbert("تم گندو ہو")  # Auto-transliterated
        0.968
    """
    if detect_urdu_script(text):
        text = transliterate_urdu_to_roman(text)

    enc = tokenizer(
        text,
        padding="max_length",
        truncation=True,
        max_length=max_length,
        return_tensors="pt",
    )
    enc = {k: v.to(device) for k, v in enc.items()}

    with torch.no_grad():
        outputs = model(**enc)
        probs = torch.softmax(outputs.logits, dim=-1)
        p_toxic = probs[0, 1].item()
    return float(p_toxic)



def mask_word(text: str, word: str, strategy: str = 'remove') -> str:
    """
    Mask a specific word in text for differential scoring.

    Args:
        text: Input text
        word: Word to mask
        strategy: 'remove' (delete word) or 'neutral' (replace with "something")

    Returns:
        Text with word masked

    Examples:
        >>> mask_word("tum gandu ho", "gandu", "remove")
        'tum ho'
        >>> mask_word("tum gandu ho", "gandu", "neutral")
        'tum something ho'
    """
    import re
    pattern = r'\b' + re.escape(word) + r'\b'

    if strategy == 'remove':
        masked = re.sub(pattern, '', text, flags=re.IGNORECASE)
        masked = re.sub(r'\s+', ' ', masked).strip()
    else:
        masked = re.sub(pattern, 'something', text, flags=re.IGNORECASE)

    return masked


def contains_word_in_lexicon(word: str) -> bool:
    """
    Check if a specific word is in RUHSOLD lexicon using fuzzy matching.

    Args:
        word: Word to check

    Returns:
        True if word matches any lexicon entry (with fuzzy patterns)

    Examples:
        >>> contains_word_in_lexicon("gandu")
        True
        >>> contains_word_in_lexicon("ganduuu")  # Fuzzy match
        True
        >>> contains_word_in_lexicon("hello")
        False
    """
    test_text = f" {word} "
    return bool(LEXICON_PATTERN.search(test_text))


def identify_toxic_words_robust(
    text: str,
    top_k: int = 5,
    lexicon_check: bool = True,
    delta_threshold: float = 0.20
) -> list:
    """
    Robust toxic word identification using lexicon-first + hybrid scoring.

    This function eliminates false positives by testing words using THREE methods:
    1. Lexicon check (fast path)
    2. Differential scoring (does removing word reduce toxicity?)
    3. Individual scoring (is word itself toxic in isolation?)

    The hybrid approach (2+3) solves the multi-toxic-word problem where removing
    one toxic word might not reduce toxicity if other toxic words remain.

    Algorithm:
        1. Get baseline toxicity of full sentence
        2. For each high-attention word:
           a. Fast path: Check if in RUHSOLD lexicon → TOXIC
           b. Differential: Remove word and re-score → If Δ > threshold → TOXIC
           c. Individual: Score word in isolation → If p_toxic > 50% → TOXIC

    Args:
        text: Input text
        top_k: Maximum toxic words to return (default: 5)
        lexicon_check: If True, use lexicon as fast path (default: True)
        delta_threshold: Minimum toxicity reduction to consider word toxic (default: 0.15)

    Returns:
        List of (word, confidence, source) tuples
        - word: The toxic word
        - confidence: 0.0-1.0 score (1.0 for lexicon, varies for differential/individual)
        - source: 'lexicon', 'differential', or 'individual'

    Examples:
        >>> identify_toxic_words_robust("tum gandu ho")
        [('gandu', 1.0, 'lexicon')]

        >>> identify_toxic_words_robust("c++ kya kutti aur badtameez cheez hai")
        [('badtameez', 0.996, 'individual'), ('kutti', 1.0, 'lexicon')]
        # badtameez caught by individual scoring (negative differential delta)
        # kya, cheez, aur filtered out (low individual toxicity)
    """
    baseline_toxic = predict_proba_mbert(text)

    if baseline_toxic < 0.5:
        return []

    tokens, attention_scores, input_ids, _ = extract_attention_weights(text)
    attention_words = map_tokens_to_words(tokens, attention_scores, input_ids)

    if not attention_words:
        return []

    max_score = max(score for _, score, _ in attention_words)
    attention_words = [
        (word, score / max_score)
        for word, score, _ in attention_words
        if score / max_score >= 0.05
    ]

    toxic_identified = []
    words_to_test = []

    for word, attention_score in attention_words:
        if len(word) <= 2:
            continue

        if lexicon_check and contains_word_in_lexicon(word):
            toxic_identified.append((word, 1.0, 'lexicon'))
            continue

        words_to_test.append((word, attention_score))

    if words_to_test:
        masked_texts = [mask_word(text, word, strategy='remove') for word, _ in words_to_test]
        isolated_words = [word for word, _ in words_to_test]

        masked_toxics = predict_proba_mbert_batch(masked_texts)
        individual_toxics = predict_proba_mbert_batch(isolated_words)

        for (word, attention_score), masked_toxic, individual_toxic in zip(
            words_to_test, masked_toxics, individual_toxics
        ):
            delta = baseline_toxic - masked_toxic


            is_toxic = False
            confidence = 0.0
            source = 'differential'

            if individual_toxic >= 0.5:
                confidence = individual_toxic
                is_toxic = True
                source = 'individual'

            elif delta >= delta_threshold:
                confidence = min(delta / 0.5, 1.0)
                is_toxic = True
                source = 'differential'

            if is_toxic:
                toxic_identified.append((word, confidence, source))

    toxic_identified.sort(key=lambda x: x[1], reverse=True)
    return toxic_identified[:top_k]



TOXICITY_BLOCK_THRESHOLD = 0.90
TOXICITY_SANITIZE_THRESHOLD = 0.60

def filter_prompt(
    text: str,
    extract_words: bool = True,
    block_threshold: float = None,
    sanitize_threshold: float = None
) -> dict:
    """
    Core pipeline step: classify + lexicon check + attention attribution + decide action.

    Args:
        text: Input text (Roman Urdu or Urdu script)
        extract_words: If True, extract toxic words using attention (default: True)
        block_threshold: Custom block threshold (default: use TOXICITY_BLOCK_THRESHOLD)
        sanitize_threshold: Custom sanitize threshold (default: use TOXICITY_SANITIZE_THRESHOLD)

    Returns a dict:
    {
        "original_text": str,              # Original user input
        "is_urdu_script": bool,            # True if Urdu script detected
        "transliterated_text": str | None, # Roman Urdu (None if already Roman)
        "clean_text": str,                 # Sanitized or blocked text
        "p_toxic": float,                  # Toxicity probability [0.0, 1.0]
        "contains_lexicon": bool,          # Hate word detected
        "action": str,                     # "allow" | "sanitize" | "block"
        "toxic_words": list[tuple],        # [(word, score), ...] if extract_words=True
    }

    Examples:
        >>> filter_prompt("tum gandu ho")
        {
            "original_text": "tum gandu ho",
            "is_urdu_script": False,
            "transliterated_text": None,
            "p_toxic": 0.971,
            "action": "block",
            "toxic_words": [("gandu", 0.82), ("tum", 0.15)]
        }

        >>> filter_prompt("تم سور ہو")
        {
            "original_text": "تم سور ہو",
            "is_urdu_script": True,
            "transliterated_text": "tm sor ho",
            "p_toxic": 0.95,
            "action": "sanitize",
            "toxic_words": [("sor", 0.75)]
        }
    """
    _block_threshold = block_threshold if block_threshold is not None else TOXICITY_BLOCK_THRESHOLD
    _sanitize_threshold = sanitize_threshold if sanitize_threshold is not None else TOXICITY_SANITIZE_THRESHOLD

    is_urdu_script = detect_urdu_script(text)
    transliterated_text = None
    if is_urdu_script:
        transliterated_text = transliterate_urdu_to_roman(text)

    text_for_processing = transliterated_text if transliterated_text else text

    p = predict_proba_mbert(text_for_processing)
    has_lex = contains_lexicon(text_for_processing)

    toxic_words = []
    toxic_words_with_source = []
    if extract_words and p >= _sanitize_threshold:
        toxic_words_with_source = identify_toxic_words_robust(
            text_for_processing,
            top_k=5,
            delta_threshold=0.20
        )
        toxic_words = [(word, confidence) for word, confidence, source in toxic_words_with_source]

    action = "allow"
    clean_text = text

    if p >= _block_threshold:
        action = "block"
        clean_text = ""
    elif p >= _sanitize_threshold or has_lex:
        action = "sanitize"
        clean_text = sanitize_text(text_for_processing, toxic_words=toxic_words)
    else:
        action = "allow"
        clean_text = text

    return {
        "original_text": text,
        "is_urdu_script": is_urdu_script,
        "transliterated_text": transliterated_text,
        "clean_text": clean_text,
        "p_toxic": p,
        "contains_lexicon": has_lex,
        "action": action,
        "toxic_words": toxic_words,
    }


if __name__ == "__main__":
    samples = [
        "tum bohat gande insan ho",
        "lanat hai tum pe gandu",
        "bohat shukriya, bohat acha content tha",
    ]
    for s in samples:
        out = filter_prompt(s)
        print("\nInput:", s)
        print("Decision:", out["action"], "| p_toxic=", f"{out['p_toxic']:.3f}")
        print("Clean text:", out["clean_text"])
