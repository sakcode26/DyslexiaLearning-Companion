import streamlit as st
from gtts import gTTS
import os
import tempfile

# List of words to practice
word_list = ["cat", "dog", "apple", "banana", "nation", "leader"]

# ✅ Ensure session state variables are initialized
if "current_index" not in st.session_state:
    st.session_state.current_index = 0
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# Function to generate speech using gTTS
def read_word():
    word = word_list[st.session_state.current_index]
    tts = gTTS(word, lang="en")
    
    # Save to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        tts.save(temp_audio.name)
        temp_filename = temp_audio.name

    # Play the audio in Streamlit
    st.audio(temp_filename, format="audio/mp3")

# Function to check spelling
def check_spelling():
    user_input = st.session_state.user_input.strip()
    correct_word = word_list[st.session_state.current_index]

    if user_input.lower() == correct_word.lower():
        st.success("✅ Correct! Great job!")
    else:
        st.error(f"❌ Incorrect! The correct word is: **{correct_word}**")

# Function to move to the next word
def next_word():
    if st.session_state.current_index < len(word_list) - 1:
        st.session_state.current_index += 1
    else:
        st.session_state.current_index = 0  # Restart from the beginning
        st.success("🎉 You've completed the practice! Restarting...")

    st.session_state.user_input = ""  # ✅ Reset input safely

# Function to move to the previous word
def prev_word():
    if st.session_state.current_index > 0:
        st.session_state.current_index -= 1

    st.session_state.user_input = ""  # ✅ Reset input safely

# Writing Assistance Module UI
def writing_assistance():
    st.title("✍️ Writing Assistance - Spelling Practice")
    st.write("Listen to the word and type it correctly.")

    word = word_list[st.session_state.current_index]

    # 🔊 Listen Button
    if st.button("🔊 Listen to Word"):
        read_word()

    # ✍️ User Input (binds to session state)
    st.text_input("Type the word here:", key="user_input")

    # ✅ Check Spelling Button
    if st.button("✅ Check Spelling"):
        check_spelling()

    # 🔄 Navigation Buttons
    col1, col2 = st.columns(2)

    with col1:
        st.button("⬅ Previous", on_click=prev_word)

    with col2:
        st.button("➡ Next", on_click=next_word)

# Run the app
writing_assistance()
