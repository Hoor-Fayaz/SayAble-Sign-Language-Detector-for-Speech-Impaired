import os
import pickle
import mediapipe as mp
import cv2

# MediaPipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

# Data directory for digits
DATA_DIR = './digit_data'

data = []
labels = []

# Only consider folders named 0 to 9
digit_classes = [str(i) for i in range(10)]

for dir_ in sorted(os.listdir(DATA_DIR)):
    if dir_ not in digit_classes:
        continue  # Skip any non-digit folders

    print(f'Processing folder: {dir_}')
    dir_path = os.path.join(DATA_DIR, dir_)

    for img_path in os.listdir(dir_path):
        data_aux = []
        x_ = []
        y_ = []

        img = cv2.imread(os.path.join(dir_path, img_path))
        if img is None:
            continue  # skip unreadable images

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for lm in hand_landmarks.landmark:
                    x_.append(lm.x)
                    y_.append(lm.y)

                for lm in hand_landmarks.landmark:
                    data_aux.append(lm.x - min(x_))
                    data_aux.append(lm.y - min(y_))

            data.append(data_aux)
            labels.append(dir_)  # 0–9 label

# Save as pickle
with open('digit_data.pickle', 'wb') as f:
    pickle.dump({'data': data, 'labels': labels}, f)

print("✅ Digit dataset saved as 'digit_data.pickle'")
