import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import pyttsx3
import speech_recognition as sr
import random
from gtts import gTTS
import tempfile
import os
import pickle

# Initialize TTS engine
tts = pyttsx3.init()
tts.setProperty('rate', 150)

# Load Gesture Recognition Model
with open('sign_model.p', 'rb') as f:
    gesture_model = pickle.load(f)

# MediaPipe Hands for Gesture Recognition
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Labels Dictionary for Gesture Recognition
labels_dict = {i: chr(65 + i) for i in range(26)}

# Sample Texts for Reading Assistance
sample_texts = [
    "The quick brown fox jumps over the lazy dog.",
    "Artificial Intelligence is transforming the world.",
    "Reading is a great way to expand your knowledge.",
    "Machine learning helps computers learn from data."
]
if "current_text" not in st.session_state:
    st.session_state.current_text = sample_texts[0]

def next_text():
    current_index = sample_texts.index(st.session_state.current_text)
    if current_index < len(sample_texts) - 1:
        st.session_state.current_text = sample_texts[current_index + 1]
    else:
        st.session_state.current_text = sample_texts[0]

def check_pronunciation():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("🎤 Speak now...")
        try:
            audio = recognizer.listen(source, timeout=5)
            spoken_text = recognizer.recognize_google(audio)
            if spoken_text.lower() == st.session_state.current_text.lower():
                st.success("✅ Pronunciation is correct!")
            else:
                st.error(f"❌ Incorrect pronunciation! You said: {spoken_text}")
        except sr.UnknownValueError:
            st.error("❌ Couldn't understand your speech. Try again!")
        except sr.RequestError:
            st.error("❌ Speech recognition service unavailable.")

def text_to_speech(text):
    tts = gTTS(text, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        tts.save(temp_audio.name)
        return temp_audio.name

def reading_assistance():
    st.title("📖 Reading Assistance")
    st.text_area("Text for Reading:", st.session_state.current_text, height=150)

    if st.button("🔊 Read Text"):
        audio_file = text_to_speech(st.session_state.current_text)
        st.audio(audio_file, format="audio/mp3")

    if st.button("🎤 Check Pronunciation"):
        check_pronunciation()
    
    if st.button("➡ Next Text"):
        next_text()

def writing_assistance():
    word_list = ["cat", "dog", "apple", "banana", "nation", "leader"]
    if "current_index" not in st.session_state:
        st.session_state.current_index = 0
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""

    st.title("✍️ Writing Assistance - Spelling Practice")
    word = word_list[st.session_state.current_index]
    
    if st.button("🔊 Listen to Word"):
        audio_file = text_to_speech(word)
        st.audio(audio_file, format="audio/mp3")

    st.text_input("Type the word here:", key="user_input")

    if st.button("✅ Check Spelling"):
        if st.session_state.user_input.strip().lower() == word.lower():
            st.success("✅ Correct! Great job!")
        else:
            st.error(f"❌ Incorrect! The correct word is: **{word}**")

    if st.button("➡ Next Word"):
        if st.session_state.current_index < len(word_list) - 1:
            st.session_state.current_index += 1
        else:
            st.session_state.current_index = 0

def main():
    st.sidebar.title("📌 Select Module")
    choice = st.sidebar.radio("Go to", ["Gesture Recognition", "Emotion Recognition", "Reading Assistance", "Writing Assistance"])

    if choice == "Gesture Recognition":
        st.title("✋ Gesture Recognition")
        st.write("📷 Ensure webcam access is enabled.")
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                st.error("Failed to capture frame.")
                break
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    landmark_data = np.array([(lm.x, lm.y) for lm in hand_landmarks.landmark]).flatten()
                    if len(landmark_data) == gesture_model.n_features_in_:
                        prediction = gesture_model.predict([landmark_data])
                        predicted_letter = labels_dict[int(prediction[0])]
                        cv2.putText(frame, predicted_letter, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
            st.image(frame, channels="RGB")
        cap.release()

    elif choice == "Emotion Recognition":
        st.title("😊 Emotion Recognition (Coming Soon)")
        st.write("🔬 AI Model is in progress. Stay tuned!")

    elif choice == "Reading Assistance":
        reading_assistance()

    elif choice == "Writing Assistance":
        writing_assistance()

if __name__ == "__main__":
    main()
