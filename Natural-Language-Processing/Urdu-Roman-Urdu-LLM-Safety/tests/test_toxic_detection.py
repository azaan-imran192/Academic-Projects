"""
Test differential scoring with the user's example:
"c++ kya kutti aur badtameez cheez hai"

Expected:
- Only kutti and badtameez should be flagged as toxic
- kya, cheez, aur should NOT be flagged (grammatical words)
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.toxic_filter import filter_prompt, identify_toxic_words_robust

def test_user_example():
    """Test the exact example from the user's screenshot"""

    if sys.platform == 'win32':
        os.system('')
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except:
            pass

    text = "c++ kya kutti aur badtameez cheez hai"

    print("="*70)
    print("DIFFERENTIAL SCORING TEST - User's Example")
    print("="*70)
    print(f"\nInput: '{text}'")
    print()
    print("Expected toxic words: kutti, badtameez (2 words)")
    print("Expected safe words: c++, kya, aur, cheez, hai (5 words)")
    print()
    print("-"*70)

    print("\n1. Testing identify_toxic_words_robust()...")
    toxic_words_robust = identify_toxic_words_robust(text, top_k=10, delta_threshold=0.20)

    print(f"\nFound {len(toxic_words_robust)} toxic words:")
    for word, confidence, source in toxic_words_robust:
        print(f"  • {word:<15} {confidence:>6.1%}  ({source})")

    toxic_word_set = {word.lower() for word, _, _ in toxic_words_robust}

    print("\n" + "-"*70)
    print("\n2. Verification:")

    expected_toxic = {'kutti', 'badtameez'}
    found_toxic = expected_toxic & toxic_word_set
    missed_toxic = expected_toxic - toxic_word_set

    print(f"  ✓ Expected toxic words found: {found_toxic}")
    if missed_toxic:
        print(f"  ✗ Missed toxic words: {missed_toxic}")

    expected_safe = {'c++', 'kya', 'aur', 'cheez', 'hai'}
    false_positives = expected_safe & toxic_word_set

    if false_positives:
        print(f"  ✗ FALSE POSITIVES (should NOT be flagged): {false_positives}")
    else:
        print(f"  ✓ No false positives! Safe words correctly ignored.")

    print("\n" + "-"*70)
    print("\n3. Testing full filter_prompt() pipeline...")

    result = filter_prompt(text, extract_words=True)

    print(f"\n  Toxicity: {result['p_toxic']:.2%}")
    print(f"  Action: {result['action'].upper()}")
    print(f"  Original: {result['original_text']}")
    print(f"  Sanitized: {result['clean_text']}")

    if result.get('toxic_words'):
        print(f"\n  Toxic words in result:")
        for word, confidence in result['toxic_words']:
            print(f"    • {word:<15} {confidence:>6.1%}")

    print("\n" + "="*70)
    print("FINAL RESULT:")
    print("="*70)

    success = True

    if len(found_toxic) == len(expected_toxic):
        print("✅ All toxic words identified")
    else:
        print(f"❌ Missing toxic words: {missed_toxic}")
        success = False

    if not false_positives:
        print("✅ No false positives (grammatical words correctly kept)")
    else:
        print(f"❌ False positives found: {false_positives}")
        success = False

    if 'kutti' in result['clean_text'] or 'badtameez' in result['clean_text']:
        print("❌ Toxic words not sanitized properly")
        success = False
    else:
        print("✅ Toxic words successfully sanitized")

    if success:
        print("\n🎉 ALL TESTS PASSED! Differential scoring is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check output above.")

    print("="*70)
    return success

if __name__ == "__main__":
    test_user_example()
