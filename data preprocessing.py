import os
import pickle
import mediapipe as mp
import cv2
import numpy as np

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

DATA_DIR = 'D:\STUDY\Major Project\project'
data, labels = [], []

for label in os.listdir(DATA_DIR):
    class_path = os.path.join(DATA_DIR, label)
    
    for img_file in os.listdir(class_path):
        img = cv2.imread(os.path.join(class_path, img_file))
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]  # Take first detected hand
            landmark_data = np.array([(lm.x, lm.y) for lm in hand_landmarks.landmark]).flatten()
            
            data.append(landmark_data)
            labels.append(label)

# Save processed data
with open('dataset.pickle', 'wb') as f:
    pickle.dump({'data': np.array(data), 'labels': np.array(labels)}, f)

print("Dataset creation completed.")
