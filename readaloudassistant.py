import speech_recognition as sr
import pyttsx3
import difflib
import sys
sys.stdout.reconfigure(encoding='utf-8')


# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Target sentence for comparison
TARGET_SENTENCE = "The quick brown fox jumps over the lazy dog."

def speak(text):
    """ Converts text to speech """
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    """ Captures audio from the microphone and converts it to text """
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("\n🎤 Speak now...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        # Recognize speech using Google Speech-to-Text
        spoken_text = recognizer.recognize_google(audio)
        print(f"🗣 You said: {spoken_text}\n")
        return spoken_text
    except sr.UnknownValueError:
        print("❌ Sorry, I could not understand the audio.")
        return None
    except sr.RequestError:
        print("❌ Error connecting to Speech API.")
        return None

def compare_text(spoken_text, target_text):
    """ Compares spoken text with the correct sentence and highlights mistakes """
    spoken_words = spoken_text.split()
    target_words = target_text.split()

    differences = []
    for i, word in enumerate(spoken_words):
        if i < len(target_words) and word.lower() != target_words[i].lower():
            differences.append(f"**{word}**")  # Highlight incorrect words
        else:
            differences.append(word)

    return " ".join(differences)

def main():
    print("\n🔹 Read-Aloud Assistant 🔹")
    print(f"📖 Read this sentence: \"{TARGET_SENTENCE}\"")
    
    speak("Please read the following sentence aloud.")
    speak(TARGET_SENTENCE)
    
    spoken_text = recognize_speech()
    
    if spoken_text:
        feedback = compare_text(spoken_text, TARGET_SENTENCE)
        print(f"\n📢 Feedback: {feedback}\n")
        speak("Here's your feedback.")
        speak(feedback)

if __name__ == "__main__":
    main()
