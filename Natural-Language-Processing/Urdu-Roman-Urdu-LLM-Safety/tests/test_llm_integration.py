"""
Test script to verify LLM integration is working correctly.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_llm_import():
    """Test if google-generativeai is installed"""
    print("="*70)
    print("TEST 1: Checking google-generativeai package")
    print("="*70)
    try:
        import google.generativeai as genai
        print("✅ google-generativeai is installed")
        print(f"   Version: {genai.__version__ if hasattr(genai, '__version__') else 'unknown'}")
        return True
    except ImportError as e:
        print("❌ google-generativeai is NOT installed")
        print(f"   Error: {e}")
        print("\n   Install with: pip install google-generativeai")
        return False

def test_llm_client_import():
    """Test if GeminiLLM class can be imported"""
    print("\n" + "="*70)
    print("TEST 2: Importing GeminiLLM class")
    print("="*70)
    try:
        from src.llm_client import GeminiLLM
        print("✅ GeminiLLM class imported successfully")
        return True
    except ImportError as e:
        print("❌ Failed to import GeminiLLM")
        print(f"   Error: {e}")
        return False

def test_api_key():
    """Test if API key is available"""
    print("\n" + "="*70)
    print("TEST 3: Checking for API key")
    print("="*70)

    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key:
        print("✅ GOOGLE_API_KEY environment variable is set")
        print("   Key value is not logged.")
        return api_key
    else:
        print("⚠️  GOOGLE_API_KEY environment variable is NOT set")
        print("   You'll need to provide it in the Streamlit sidebar")
        return None

def test_llm_generation(api_key=None):
    """Test actual LLM generation"""
    print("\n" + "="*70)
    print("TEST 4: Testing LLM generation")
    print("="*70)

    if not api_key:
        api_key = input("\nEnter your Google API key (or press Enter to skip): ").strip()
        if not api_key:
            print("⏭️  Skipping LLM generation test (no API key provided)")
            return

    try:
        from src.llm_client import GeminiLLM

        print("Initializing GeminiLLM...")
        llm = GeminiLLM(api_key=api_key)
        print("✅ GeminiLLM initialized successfully")

        print("\nGenerating test response...")
        test_prompt = "Python kya hai?"
        response = llm.generate(test_prompt, max_tokens=50)

        print("✅ LLM generation successful!")
        print(f"\nPrompt: {test_prompt}")
        print(f"Response: {response}")

    except Exception as e:
        print(f"❌ LLM generation failed")
        print(f"   Error: {str(e)}")

        if "API_KEY_INVALID" in str(e):
            print("\n   💡 Your API key appears to be invalid")
            print("   Get a valid key at: https://aistudio.google.com/app/apikey")
        elif "quota" in str(e).lower():
            print("\n   💡 API quota exceeded")
            print("   Wait a moment and try again")

def main():
    """Run all tests"""
    print("\n" + "╔" + "="*68 + "╗")
    print("║" + " "*20 + "LLM INTEGRATION TEST SUITE" + " "*22 + "║")
    print("╚" + "="*68 + "╝")

    package_ok = test_llm_import()
    if not package_ok:
        print("\n" + "="*70)
        print("CRITICAL: Install google-generativeai first!")
        print("="*70)
        return

    import_ok = test_llm_client_import()
    if not import_ok:
        return

    api_key = test_api_key()

    test_llm_generation(api_key)

    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print("1. Package installed:", "✅" if package_ok else "❌")
    print("2. GeminiLLM imports:", "✅" if import_ok else "❌")
    print("3. API key available:", "✅" if api_key else "⚠️ ")
    print("\nIf all tests pass, LLM integration should work in Streamlit!")
    print("="*70)

if __name__ == "__main__":
    main()
