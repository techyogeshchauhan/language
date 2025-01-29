import streamlit as st
import time
from lingua import Language, LanguageDetectorBuilder
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Advanced Language Detector",
    page_icon="🌎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .stTextInput > div > div > input {
        font-size: 18px;
    }
    .main-header {
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .result-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #f0f8ff;
        margin: 10px 0;
    }
    .language-confidence {
        font-size: 24px;
        font-weight: bold;
        color: #1e90ff;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'example_text' not in st.session_state:
    st.session_state.example_text = ""

def get_all_languages():
    """Get dictionary of supported languages"""
    return {
        'English': Language.ENGLISH,
        'French': Language.FRENCH,
        'German': Language.GERMAN,
        'Spanish': Language.SPANISH,
        'Portuguese': Language.PORTUGUESE,
        'Italian': Language.ITALIAN,
        'Russian': Language.RUSSIAN,
        'Arabic': Language.ARABIC,
        'Hindi': Language.HINDI,
        'Chinese': Language.CHINESE,
        'Japanese': Language.JAPANESE,
        'Korean': Language.KOREAN,
        'Vietnamese': Language.VIETNAMESE,
        'Thai': Language.THAI,
        'Dutch': Language.DUTCH,
        'Greek': Language.GREEK,
        'Turkish': Language.TURKISH,
        'Polish': Language.POLISH,
        'Danish': Language.DANISH,
        'Finnish': Language.FINNISH,
        'Hungarian': Language.HUNGARIAN,
        'Swedish': Language.SWEDISH,
        'Indonesian': Language.INDONESIAN,
        'Romanian': Language.ROMANIAN,
        'Bengali': Language.BENGALI,
        'Persian': Language.PERSIAN
    }

# Example texts
EXAMPLE_TEXTS = {
    "English": "Hello! How are you doing today? I hope you're having a wonderful day filled with joy and happiness.",
    "French": "Bonjour! Comment allez-vous aujourd'hui? J'espère que vous passez une merveilleuse journée remplie de joie et de bonheur.",
    "Spanish": "¡Hola! ¿Cómo estás hoy? Espero que estés teniendo un día maravilloso lleno de alegría y felicidad.",
    "German": "Hallo! Wie geht es dir heute? Ich hoffe, du hast einen wunderbaren Tag voller Freude und Glück.",
    "Italian": "Ciao! Come stai oggi? Spero che tu stia passando una giornata meravigliosa piena di gioia e felicità.",
    "Russian": "Привет! Как ты сегодня? Надеюсь, у тебя прекрасный день, полный радости и счастья.",
    "Japanese": "こんにちは！今日の調子はどうですか？喜びと幸せに満ちた素晴らしい一日をお過ごしください。",
    "Chinese": "你好！今天好吗？希望你度过充满欢乐和幸福的美好一天。",
    "Arabic": "مرحبا! كيف حالك اليوم؟ أتمنى أن تقضي يومًا رائعًا مليئًا بالفرح والسعادة.",
    "Hindi": "नमस्ते! आज आप कैसे हैं? मुझे आशा है कि आपका दिन खुशी और आनंद से भरा हो।"
}

def detect_language_with_confidence(text, detector):
    """Detect language and return confidence scores"""
    try:
        detected_lang = detector.detect_language_of(text)
        if not detected_lang:
            return None, []
            
        confidences = detector.compute_language_confidence_values(text)
        sorted_confidences = sorted(confidences, key=lambda x: x[1], reverse=True)
        
        return detected_lang, sorted_confidences
    except Exception as e:
        st.error(f"Error in language detection: {str(e)}")
        return None, []

def save_to_history(text, detected_lang, confidence):
    """Save detection results to history"""
    st.session_state.history.append({
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'text': text[:50] + '...' if len(text) > 50 else text,
        'detected_language': detected_lang.name if detected_lang else 'Unknown',
        'confidence': f"{confidence:.2%}" if confidence else 'N/A'
    })

def show_history():
    """Display detection history"""
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.dataframe(df, hide_index=True)
    else:
        st.info("No detection history yet")

def main():
    # Sidebar
    with st.sidebar:
        st.header("📊 Detection History")
        if st.button("Clear History"):
            st.session_state.history = []
        show_history()

    # Main content
    st.markdown("<h1 class='main-header'>🌎 Advanced Language Detection</h1>", unsafe_allow_html=True)
    
    # Initialize detector
    languages = get_all_languages()
    detector = LanguageDetectorBuilder.from_languages(*languages.values()).build()

    # Examples and text input sections
    col1, col2 = st.columns([2, 1])

    with col2:
        st.markdown("### 📝 Example Texts")
        selected_example = st.selectbox(
            "Select a language example",
            list(EXAMPLE_TEXTS.keys())
        )
        if st.button("Load Example"):
            st.session_state.example_text = EXAMPLE_TEXTS[selected_example]

    with col1:
        text_input = st.text_area(
            "Enter text to detect language:",
            value=st.session_state.example_text,
            height=150,
            help="Enter or paste the text you want to analyze"
        )

    # Detection button and minimum length warning
    min_length = 20
    col1, col2 = st.columns([2, 1])
    with col1:
        detect_button = st.button("🔍 Detect Language", type="primary", 
                                disabled=len(text_input.strip()) < min_length)
    with col2:
        if len(text_input.strip()) < min_length:
            st.warning(f"Please enter at least {min_length} characters for accurate detection")

    # Process detection
    if detect_button and text_input.strip():
        with st.spinner("Analyzing text..."):
            time.sleep(0.5)  # UX improvement
            detected_lang, confidences = detect_language_with_confidence(text_input, detector)

            if detected_lang and confidences:
                # Save to history
                main_confidence = next((conf for lang, conf in confidences if lang == detected_lang), 0)
                save_to_history(text_input, detected_lang, main_confidence)

                # Display results
                st.markdown("### 📊 Detection Results")
                
                # Main result
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(
                        f"""
                        <div class='result-box'>
                            <h3>Detected Language</h3>
                            <p class='language-confidence'>{detected_lang.name}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                with col2:
                    st.markdown(
                        f"""
                        <div class='result-box'>
                            <h3>Confidence Score</h3>
                            <p class='language-confidence'>{main_confidence:.2%}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                # Top matches
                st.markdown("### 🎯 Top Language Matches")
                for lang, conf in confidences[:5]:
                    st.markdown(
                        f"""
                        <div style="
                            background-color: {'#e6f3ff' if lang == detected_lang else '#ffffff'};
                            padding: 15px;
                            border-radius: 5px;
                            margin: 5px 0;
                            border: 1px solid {'#1e90ff' if lang == detected_lang else '#ddd'};
                        ">
                            <strong>{lang.name}</strong>: {conf:.2%}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.error("Could not detect the language. Please try with different text.")

    # Show supported languages
    with st.expander("🌍 Supported Languages"):
        cols = st.columns(4)
        for idx, lang in enumerate(sorted(languages.keys())):
            cols[idx % 4].markdown(f"- {lang}")

if __name__ == "__main__":
    main()