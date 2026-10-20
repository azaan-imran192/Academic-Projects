"""
Streamlit Demo App for Toxic Prompt Filter
A user-friendly web interface for testing the Urdu/Roman-Urdu toxicity filter
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from src.toxic_filter import filter_prompt, predict_proba_mbert
from src.llm_client import GeminiLLM

st.set_page_config(
    page_title="Urdu Toxic Filter",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color:
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color:
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color:
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown('<p class="main-header">🛡️ Urdu Toxic Prompt Filter</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Filter toxic content in Urdu and Roman-Urdu text with AI</p>', unsafe_allow_html=True)

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Settings")

    # API Key input
    try:
        configured_key = os.getenv("GOOGLE_API_KEY") or st.secrets.get("GOOGLE_API_KEY", "")
    except (FileNotFoundError, st.errors.StreamlitSecretNotFoundError):
        configured_key = os.getenv("GOOGLE_API_KEY", "")
    google_api_key = st.text_input(
        "Google API Key",
        type="password",
        value=configured_key,
        help="Get your free API key from https://aistudio.google.com/app/apikey"
    )

    st.markdown("---")

    # Threshold sliders
    st.subheader("Filter Thresholds")
    block_threshold = st.slider(
        "Block Threshold",
        0.0, 1.0, 0.90,
        help="Texts with toxicity >= this value will be hard blocked"
    )
    sanitize_threshold = st.slider(
        "Sanitize Threshold",
        0.0, 1.0, 0.60,
        help="Texts with toxicity >= this value will be sanitized"
    )

    st.markdown("---")

    # Example texts
    st.subheader("📝 Example Texts")

    if st.button("🟢 Safe Example"):
        st.session_state.text = "Mujhe Python programming seekhni hai. Koi achi book suggest karen?"

    if st.button("🟡 Moderate Example"):
        st.session_state.text = "Tum bohat bewakoof ho, coding seekh lo pehle"

    if st.button("🔴 Toxic Example"):
        st.session_state.text = "Tum gande aur badtameez insan ho"

    st.markdown("---")

    # About section
    with st.expander("ℹ️ About"):
        st.markdown("""
        **Toxic Prompt Filter for Urdu**

        This system uses:
        - Fine-tuned mBERT for context-aware toxicity detection
        - RUHSOLD lexicon for explicit slur matching
        - Google Gemini for safe Urdu text generation

        **Team**: Azaan Imran, Ahmad Bilal Habib
        """)

col1, col2 = st.columns([2, 1])

with col1:
    text_input = st.text_area(
        "Enter text to check:",
        value=st.session_state.get('text', ''),
        height=150,
        placeholder="Type or paste Urdu/Roman-Urdu text here...\nمثال: Python programming کیا ہے؟"
    )

    col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])

    with col_btn1:
        analyze_btn = st.button("🔍 Check Toxicity", type="primary", use_container_width=True)

    with col_btn2:
        clear_btn = st.button("🗑️ Clear", use_container_width=True)
        if clear_btn:
            st.session_state.text = ""
            st.rerun()

with col2:
    st.info("""
    **How it works:**

    1. Enter text in Urdu or Roman Urdu
    2. Click "Check Toxicity"
    3. See toxicity score and action
    4. Optionally generate LLM response
    """)

# Processing
if analyze_btn:
    if text_input.strip():
        with st.spinner("Analyzing toxicity..."):
            # Filter the input with custom thresholds
            result = filter_prompt(
                text_input,
                block_threshold=block_threshold,
                sanitize_threshold=sanitize_threshold
            )
            # Store result in session state for LLM generation
            st.session_state.last_result = result
            st.session_state.last_text = text_input
            st.session_state.last_block_threshold = block_threshold
            st.session_state.last_sanitize_threshold = sanitize_threshold
    else:
        st.warning("⚠️ Please enter some text to analyze.")

# Display results (outside button click so it persists)
if 'last_result' in st.session_state:
    result = st.session_state.last_result

    # Display results
    st.markdown("---")
    st.subheader("📊 Analysis Results")

    # Metrics in columns
    metric_col1, metric_col2, metric_col3 = st.columns(3)

    with metric_col1:
        toxicity_color = "🔴" if result['p_toxic'] >= 0.90 else "🟡" if result['p_toxic'] >= 0.60 else "🟢"
        st.metric(
            "Toxicity Score",
            f"{toxicity_color} {result['p_toxic']:.2%}",
            delta=None
        )

    with metric_col2:
        action_icons = {
            "allow": "🟢",
            "sanitize": "🟡",
            "block": "🔴"
        }
        action_labels = {
            "allow": "ALLOW",
            "sanitize": "SANITIZE",
            "block": "BLOCK"
        }
        st.metric(
            "Action",
            f"{action_icons[result['action']]} {action_labels[result['action']]}",
            delta=None
        )

    with metric_col3:
        lexicon_icon = "⚠️" if result['contains_lexicon'] else "✅"
        lexicon_text = "Yes" if result['contains_lexicon'] else "No"
        st.metric(
            "Contains Hate Words",
            f"{lexicon_icon} {lexicon_text}",
            delta=None
        )

    # Show detailed results
    if result['action'] == 'block':
        st.error("⛔ **BLOCKED**: This text contains highly toxic content and has been blocked.")

    elif result['action'] == 'sanitize':
        st.warning("⚠️ **SANITIZED**: Offensive words have been replaced.")
        col_orig, col_clean = st.columns(2)
        with col_orig:
            st.markdown("**Original Text:**")
            st.code(result['original_text'])
        with col_clean:
            st.markdown("**Sanitized Text:**")
            st.code(result['clean_text'])

    else:
        st.success("✅ **ALLOWED**: This text is safe and contains no toxic content.")

    # Show toxic words if available (NEW FEATURE)
    if result.get('toxic_words'):
        st.markdown("---")
        st.subheader("🔍 Toxic Words Detected")
        st.markdown("These words contributed to the toxicity score:")

        for word, score in result['toxic_words']:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{word}**")
            with col2:
                st.markdown(f"`{score:.1%}`")

        # Optional: Visual highlighting
        if result['action'] in ['sanitize', 'block']:
            with st.expander("📊 Visual Contribution Analysis"):
                text_for_display = result.get('transliterated_text') or result['original_text']
                toxic_word_dict = {word.lower(): score for word, score in result['toxic_words']}

                highlighted_html = ""
                for word in text_for_display.split():
                    word_clean = word.lower().strip('.,!?')
                    if word_clean in toxic_word_dict:
                        score = toxic_word_dict[word_clean]
                        opacity = min(0.3 + score * 0.7, 1.0)
                        color = f"rgba(255, 0, 0, {opacity})"
                        highlighted_html += f'<span style="background-color: {color}; padding: 2px 4px; border-radius: 3px; margin: 2px;">{word}</span> '
                    else:
                        highlighted_html += f'{word} '

                st.markdown(highlighted_html, unsafe_allow_html=True)
                st.caption("💡 Color intensity indicates contribution to toxicity")

    # Show Urdu script info if applicable (NEW FEATURE)
    if result.get('is_urdu_script'):
        st.markdown("---")
        st.info("📝 **Urdu Script Detected**: Text was transliterated to Roman Urdu for processing")
        if result.get('transliterated_text'):
            with st.expander("View Transliteration"):
                st.code(result['transliterated_text'], language=None)

    # LLM generation section
    if result['action'] != 'block':
        st.markdown("---")
        st.subheader("🤖 Generate LLM Response")

        generate_response = st.checkbox("Generate response using Gemini", value=False)

        if generate_response:
            if google_api_key:
                with st.spinner("Generating Gemini response..."):
                    try:
                        # Initialize Gemini
                        llm = GeminiLLM(api_key=google_api_key)

                        # Generate response in Roman Urdu
                        llm_response = llm.generate(
                            result['clean_text'],
                            max_tokens=1000,
                            temperature=0.7,
                            language="roman-urdu"
                        )

                        # Verify output safety with same thresholds used for input
                        output_check = filter_prompt(
                            llm_response,
                            block_threshold=st.session_state.last_block_threshold,
                            sanitize_threshold=st.session_state.last_sanitize_threshold
                        )

                        st.markdown("**Gemini Response:**")

                        if output_check['action'] == 'block':
                            st.error("⚠️ **Output Blocked**: LLM generated toxic content. Response was filtered.")
                            st.caption(f"Output toxicity score: {output_check['p_toxic']:.2%}")
                        else:
                            st.success(llm_response)
                            st.caption(f"✅ Output verified safe (toxicity: {output_check['p_toxic']:.2%})")

                    except ImportError as e:
                        st.error("❌ **Missing Package**: google-generativeai not installed")
                        st.code("pip install google-generativeai", language="bash")
                        st.caption(f"Error details: {str(e)}")

                    except ValueError as e:
                        if "API key" in str(e):
                            st.error("❌ **Invalid API Key**: The API key you provided is invalid")
                            st.info("💡 Get a free API key at: https://aistudio.google.com/app/apikey")
                        else:
                            st.error(f"❌ **Configuration Error**: {str(e)}")

                    except Exception as e:
                        error_msg = str(e)
                        st.error(f"❌ **Error**: {error_msg}")

                        # Provide helpful hints based on error type
                        if "API_KEY_INVALID" in error_msg or "invalid api key" in error_msg.lower():
                            st.info("💡 Your API key appears to be invalid. Get a new one at: https://aistudio.google.com/app/apikey")
                        elif "quota" in error_msg.lower() or "limit" in error_msg.lower():
                            st.info("💡 API quota exceeded. Wait a moment and try again, or check your quota at: https://aistudio.google.com")
                        elif "blocked" in error_msg.lower():
                            st.info("💡 The request was blocked by Gemini's safety filters. Try rephrasing your input.")
                        else:
                            st.caption("If the problem persists, check the error message above and your API key configuration.")

            else:
                st.warning("⚠️ Please enter your Google API key in the sidebar to generate LLM responses.")
                st.info("💡 Get a free API key at: https://aistudio.google.com/app/apikey")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.9rem;'>
    <p>🛡️ Toxic Prompt Filter for Urdu and Roman-Urdu</p>
    <p>Built with mBERT + RUHSOLD Lexicon + Google Gemini</p>
    <p>Team: Azaan Imran, Ahmad Bilal Habib | NLP Project 2024-2025</p>
</div>
""", unsafe_allow_html=True)
