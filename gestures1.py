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

# Start video capture
cap = cv2.VideoCapture(0)
last_prediction = None
last_spoken_time = time.time()

print("Press 'q' to exit...")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame.")
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Extract hand landmark positions
            landmark_data = np.array([(lm.x, lm.y) for lm in hand_landmarks.landmark]).flatten()

            if len(landmark_data) == model.n_features_in_:
                prediction = model.predict([landmark_data])
                predicted_letter = labels_dict[int(prediction[0])]

                # Speak only if a new letter is detected
                if predicted_letter != last_prediction and time.time() - last_spoken_time > 1:
                    tts.say(predicted_letter)
                    tts.runAndWait()
                    last_prediction = predicted_letter
                    last_spoken_time = time.time()

                # Display letter on frame
                cv2.putText(frame, predicted_letter, (50, 100), cv2.FONT_HERSHEY_SIMPLEX,
                            2, (0, 255, 0), 3)

    # Show video feed
    cv2.imshow("Gesture Recognition", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
print("Gesture Recognition Stopped.")
