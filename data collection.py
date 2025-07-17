import os
import cv2

# Define dataset directory
DATA_DIR = "D:\STUDY\Major Project\project"
os.makedirs(DATA_DIR, exist_ok=True)  # Ensure directory exists

num_classes = 26  # A-Z letters
num_samples = 100  # Images per letter

cap = cv2.VideoCapture(0)  # Open webcam

for letter_index in range(num_classes):
    letter_dir = os.path.join(DATA_DIR, str(letter_index))
    os.makedirs(letter_dir, exist_ok=True)

    print(f'Collecting data for letter: {chr(65 + letter_index)} ({letter_index})')

    while True:
        ret, frame = cap.read()
        cv2.putText(frame, f'Show {chr(65 + letter_index)} and press "A" to start', (50, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Collecting Data', frame)

        if cv2.waitKey(1) & 0xFF == ord('a'):  # Start when 'A' is pressed
            break

    for i in range(num_samples):
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame.")
            break

        img_path = os.path.join(letter_dir, f'{i}.jpg')
        cv2.imwrite(img_path, frame)

        cv2.imshow('Collecting Data', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Quit early if 'q' is pressed
            break

print("Data collection completed.")
cap.release()
cv2.destroyAllWindows()