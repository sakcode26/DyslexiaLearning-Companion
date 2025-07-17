import streamlit as st
import pyttsx3
import speech_recognition as sr
import random
from difflib import SequenceMatcher

# Initialize TTS engine
engine = pyttsx3.init()

# List of sentences for practice
practice_sentences = [
    "Hello, how are you?",
    "This is a simple sentence.",
    "I love learning new things.",
    "Reading aloud helps me improve.",
    "Practice makes perfect."
]

# Store session state variables
if "sentence" not in st.session_state:
    st.session_state.sentence = random.choice(practice_sentences)

if "speed" not in st.session_state:
    st.session_state.speed = 150  # Default normal speed

# Function to read aloud the sentence
def read_text():
    engine.setProperty("rate", st.session_state.speed)
    engine.say(st.session_state.sentence)
    engine.runAndWait()

# Function to change reading speed
def set_speed(speed_label):
    speeds = {"Slow": 100, "Normal": 150, "Fast": 200}
    st.session_state.speed = speeds[speed_label]

# Function to get a new sentence
def new_sentence():
    st.session_state.sentence = random.choice(practice_sentences)

# Function to calculate similarity between two strings
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

# Function to check pronunciation using speech recognition
def check_pronunciation():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    with mic as source:
        st.info("🎤 Speak the sentence aloud now...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=5)
        st.success("✅ Recording complete! Processing...")

    try:
        spoken_text = recognizer.recognize_google(audio).strip().lower()
        original_text = st.session_state.sentence.strip().lower()

        # Calculate similarity
        similarity = similar(spoken_text, original_text)

        if similarity > 0.85:
            st.success("🎉 Great job! Your pronunciation is perfect!")
        else:
            st.warning(f"⚠ Oops! You said: **{spoken_text}**. Try again!")
    except sr.UnknownValueError:
        st.error("😕 Sorry, I couldn't understand your speech.")
    except sr.RequestError:
        st.error("🔌 Could not connect to Google Speech Recognition service.")

# Streamlit UI for Reading Assistance
def reading_assistance():
    st.title("📖 Reading Assistance")
    st.write("Listen to the sentence, read it aloud, and check your pronunciation.")

    st.subheader("📝 Practice Sentence:")
    st.write(f"**{st.session_state.sentence}**")

    # Read Aloud Button
    if st.button("🔊 Listen"):
        read_text()

    # Dropdown for speed selection
    speed_label = st.selectbox("Select Speed:", ["Slow", "Normal", "Fast"], index=1)
    set_speed(speed_label)

    # Get New Sentence Button
    if st.button("🔄 New Sentence"):
        new_sentence()
        st.experimental_rerun()

    # Pronunciation Check Button
    if st.button("🎤 Check Pronunciation"):
        check_pronunciation()
