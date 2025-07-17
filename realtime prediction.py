import streamlit as st
import pickle
import cv2
import mediapipe as mp
import numpy as np
import pyttsx3
import time

# Initialize text-to-speech engine
tts = pyttsx3.init()
tts.setProperty('rate', 150)  # Adjust speed

# Load trained model
with open('sign_model.p', 'rb') as f:
    model = pickle.load(f)

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Label dictionary (Mapping 0-25 to A-Z)
labels_dict = {i: chr(65 + i) for i in range(26)}

# Load letter images (Ensure images are named 'A.jpg', 'B.jpg', etc., in 'letters/' folder)
letter_images = {chr(65 + i): cv2.imread(f"letters/{chr(65 + i)}.jpg") for i in range(26)}

# Function to start gesture recognition
def gesture_recognition():
    st.write("**Gesture Recognition Started! Press 'q' to exit.**")

    cap = cv2.VideoCapture(0)
    last_prediction = None  
    last_spoken_time = time.time()  

    while True:
        ret, frame = cap.read()
        if not ret:
            st.write("Failed to capture frame.")
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                landmark_data = np.array([(lm.x, lm.y) for lm in hand_landmarks.landmark]).flatten()

                if len(landmark_data) == model.n_features_in_:
                    prediction = model.predict([landmark_data])
                    predicted_letter = labels_dict[int(prediction[0])]

                    # Display letter image
                    if predicted_letter in letter_images:
                        letter_img = letter_images[predicted_letter]
                        if letter_img is not None:
                            letter_img = cv2.resize(letter_img, (200, 200))
                            roi = frame[50:250, 50:250]
                            blended = cv2.addWeighted(roi, 0.5, letter_img, 0.5, 0)
                            frame[50:250, 50:250] = blended

                    # Speak only if a new letter is detected
                    if predicted_letter != last_prediction and time.time() - last_spoken_time > 1:
                        tts.say(predicted_letter)
                        tts.runAndWait()
                        last_prediction = predicted_letter
                        last_spoken_time = time.time()

                    cv2.putText(frame, predicted_letter, (300, 100), cv2.FONT_HERSHEY_SIMPLEX, 
                                2, (0, 255, 0), 3)

        cv2.imshow('Gesture Recognition', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
            break

    cap.release()
    cv2.destroyAllWindows()

# Streamlit UI
st.title("Gesture Recognition System")
if st.button("Start Gesture Recognition"):
    gesture_recognition()
