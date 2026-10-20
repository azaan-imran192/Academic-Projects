"""
llm_client.py

Google Gemini API client for generating Urdu language responses.
Integrates with the toxic prompt filter pipeline for safe LLM interactions.
"""

import os
import time
from typing import Optional

try:
    import google.generativeai as genai
except ImportError:
    raise ImportError(
        "google-generativeai package not installed. "
        "Install it with: pip install google-generativeai"
    )


class GeminiLLM:
    """
    Client for Google Gemini API with Urdu language support.

    Usage:
        # With API key parameter
        llm = GeminiLLM(api_key="your-api-key")

        # Or set environment variable GOOGLE_API_KEY
        llm = GeminiLLM()

        # Generate response
        response = llm.generate("Mujhe coding seekhni hai")
        print(response)
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: Optional[str] = None
    ):
        """
        Initialize Gemini API client.

        Args:
            api_key: Google API key (or set GOOGLE_API_KEY env var)
            model_name: Model to use (gemini-1.5-flash or gemini-1.5-pro)
                       gemini-1.5-flash: Fast, good Urdu support, generous free tier
                       gemini-1.5-pro: Better quality, slower, limited free quota
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key required. Either:\n"
                "1. Pass api_key parameter: GeminiLLM(api_key='your-key')\n"
                "2. Set GOOGLE_API_KEY environment variable\n"
                "Get your API key at: https://aistudio.google.com/app/apikey"
            )

        genai.configure(api_key=self.api_key)
        self.model_name = model_name or os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        self.model = genai.GenerativeModel(self.model_name)

        self.last_call_time = 0
        self.min_call_interval = 0.1

    def generate(
        self,
        prompt: str,
        max_tokens: int = 500,
        temperature: float = 0.7,
        language: str = "urdu"
    ) -> str:
        """
        Generate response from Gemini with language instruction.

        Args:
            prompt: User input text (can be Roman Urdu or Urdu script)
            max_tokens: Maximum tokens to generate (default: 150)
            temperature: Sampling temperature 0.0-1.0 (default: 0.7)
                        Lower = more deterministic, Higher = more creative
            language: Response language (default: "urdu")

        Returns:
            Generated text response in specified language

        Examples:
            >>> llm = GeminiLLM(api_key="your-key")
            >>> response = llm.generate("Python kya hai?")
            >>> print(response)
            'Python aik programming language hai...'
        """
        try:
            time_since_last_call = time.time() - self.last_call_time
            if time_since_last_call < self.min_call_interval:
                time.sleep(self.min_call_interval - time_since_last_call)

            language_instruction = {
                "urdu": "Respond in Urdu language (اردو میں جواب دیں). Give a detailed, helpful explanation.",
                "roman-urdu": "Respond in Roman Urdu (using Latin script like 'aap kaise hain'). Give a detailed, helpful explanation in 2-3 sentences.",
                "english": "Respond in English. Give a detailed, helpful explanation."
            }
            instruction = language_instruction.get(language.lower(), language_instruction["urdu"])
            full_prompt = f"{instruction}\n\nQuestion: {prompt}"

            generation_config = {
                "max_output_tokens": max_tokens,
                "temperature": temperature,
            }

            safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_ONLY_HIGH"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_ONLY_HIGH"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_ONLY_HIGH"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_ONLY_HIGH"
                }
            ]

            response = self.model.generate_content(
                full_prompt,
                generation_config=generation_config,
                safety_settings=safety_settings
            )

            self.last_call_time = time.time()

            if response.prompt_feedback.block_reason:
                return f"Error: Response blocked by Gemini safety filters (Reason: {response.prompt_feedback.block_reason})"

            if response and response.text:
                return response.text.strip()
            elif response.candidates and response.candidates[0].finish_reason:
                finish_reason = response.candidates[0].finish_reason
                if finish_reason == 1:
                    return response.text.strip() if response.text else "Error: Empty response"
                elif finish_reason == 2:
                    return response.text.strip() + " [Response truncated - increase max_tokens]"
                elif finish_reason == 3:
                    return "Error: Response blocked by safety filters"
                else:
                    return f"Error: Response incomplete (finish_reason: {finish_reason})"
            else:
                return "Error: Empty response from Gemini API"

        except Exception as e:
            error_msg = str(e)

            if "API_KEY_INVALID" in error_msg:
                return "Error: Invalid API key. Get a valid key at https://aistudio.google.com/app/apikey"
            elif "RATE_LIMIT_EXCEEDED" in error_msg or "429" in error_msg:
                return "Error: Rate limit exceeded. Free tier allows 60 requests/minute. Please wait and try again."
            elif "QUOTA_EXCEEDED" in error_msg:
                return "Error: Quota exceeded. Check your API limits at https://aistudio.google.com"
            else:
                return f"Error generating response: {error_msg}"

    def generate_safe(
        self,
        prompt: str,
        verify_callback=None,
        max_retries: int = 2,
        **kwargs
    ) -> dict:
        """
        Generate response with built-in safety verification.

        Args:
            prompt: User input text
            verify_callback: Function to verify response safety (e.g., filter_prompt)
                           Should return dict with 'action' key
            max_retries: Maximum retry attempts if response is toxic
            **kwargs: Additional arguments passed to generate()

        Returns:
            dict with keys:
                - 'response': Generated text
                - 'is_safe': Boolean indicating if response passed verification
                - 'retry_count': Number of retries needed
                - 'verification_result': Full result from verify_callback
        """
        retry_count = 0

        while retry_count <= max_retries:
            response_text = self.generate(prompt, **kwargs)

            if verify_callback is None:
                return {
                    'response': response_text,
                    'is_safe': True,
                    'retry_count': retry_count,
                    'verification_result': None
                }

            verification = verify_callback(response_text)

            if verification.get('action') != 'block':
                return {
                    'response': response_text,
                    'is_safe': True,
                    'retry_count': retry_count,
                    'verification_result': verification
                }

            retry_count += 1
            if retry_count <= max_retries:
                kwargs['temperature'] = max(0.3, kwargs.get('temperature', 0.7) - 0.2)

        return {
            'response': "Response generation failed: All attempts produced unsafe content",
            'is_safe': False,
            'retry_count': retry_count,
            'verification_result': verification
        }


def test_gemini(api_key: str = None):
    """
    Quick test function to verify Gemini API integration.

    Args:
        api_key: Optional API key (uses env var if not provided)
    """
    try:
        llm = GeminiLLM(api_key=api_key)

        test_prompts = [
            "Python programming language kya hai?",
            "Mujhe machine learning seekhni hai",
            "اردو میں کوڈنگ کیسے سیکھوں؟"
        ]

        print("Testing Gemini API Integration...")
        print("=" * 50)

        for i, prompt in enumerate(test_prompts, 1):
            print(f"\nTest {i}:")
            print(f"Prompt: {prompt}")
            response = llm.generate(prompt, max_tokens=100)
            print(f"Response: {response[:200]}...")
            print("-" * 50)

        print("\n✅ Gemini API test completed successfully!")

    except Exception as e:
        print(f"\n❌ Gemini API test failed: {e}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        test_gemini(api_key=sys.argv[1])
    else:
        test_gemini()
