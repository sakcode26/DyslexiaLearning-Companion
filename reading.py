import streamlit as st
import speech_recognition as sr
import difflib
import re

# Sample texts for reading practice
sample_texts = [
    "The quick brown fox jumps over the lazy dog.",
    "Artificial Intelligence is transforming the world.",
    "Reading is a great way to expand your knowledge.",
    "Machine learning helps computers learn from data."
]

if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "user_pronunciation" not in st.session_state:
    st.session_state.user_pronunciation = ""

# Function to clean text (remove punctuation & lowercase for comparison)
def clean_text(text):
    return re.sub(r'[^\w\s]', '', text).strip().lower()

# Speech recognition function
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        st.info("🎙 Listening... Please read the text aloud.")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=20)
            recognized_text = recognizer.recognize_google(audio)
            st.session_state.user_pronunciation = recognized_text
            check_pronunciation(recognized_text)
        except sr.UnknownValueError:
            st.error("❌ Could not understand your speech. Try again.")
        except sr.RequestError:
            st.error("❌ Could not connect to the speech recognition service.")

# Pronunciation check function (Word-by-word matching)
def check_pronunciation(spoken_text):
    correct_text = sample_texts[st.session_state.current_index]

    # Clean and normalize both texts
    spoken_clean = clean_text(spoken_text)
    correct_clean = clean_text(correct_text)

    # Use SequenceMatcher for better similarity check
    matcher = difflib.SequenceMatcher(None, correct_clean, spoken_clean)
    similarity = matcher.ratio()

    if similarity > 0.85:  # Threshold for correct pronunciation
        st.success("✅ Correct pronunciation!")
    else:
        st.error(f"❌ Incorrect pronunciation! You said: **{spoken_text}**")
        st.warning(f"🔎 Similarity Score: {round(similarity * 100, 2)}%")


# Function to move to the next text
def next_text():
    if st.session_state.current_index < len(sample_texts) - 1:
        st.session_state.current_index += 1
    else:
        st.session_state.current_index = 0  # Restart from the beginning

    st.session_state.user_pronunciation = ""

# Streamlit UI
st.title("📖 Reading Assistance - Pronunciation Checker")
st.write("Read the text aloud and check your pronunciation.")

st.text_area("Text for Reading:", sample_texts[st.session_state.current_index], height=100)

if st.button("🎙 Start Speaking"):
    recognize_speech()

if st.session_state.user_pronunciation:
    st.write("🔊 You said: ", st.session_state.user_pronunciation)

if st.button("➡ Next Text"):
    next_text()
