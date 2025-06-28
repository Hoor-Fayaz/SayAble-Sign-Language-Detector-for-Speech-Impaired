import os
import pickle
import mediapipe as mp
import cv2
import numpy as np
from collections import Counter

# MediaPipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)

# Data directory for travel & emergency
DATA_DIR = './data_communication_videos'

data = []
labels = []

# Target word classes for travel & emergency
everyday_communication = [
    "hello", "goodbye", "thank_you", "sorry", "please",
    "welcome", "fine", "excuse", "sign", "language",
    "understand", "not", "again", "slow", "write",
    "talk", "maybe", "phone", "yes", "no", "No Gesture Detected"
]


for word in sorted(os.listdir(DATA_DIR)):
    if word not in everyday_communication:
        continue

    print(f"\n🔍 Processing word: {word}")
    word_path = os.path.join(DATA_DIR, word)

    for filename in os.listdir(word_path):
        if not filename.endswith('.avi'):
            continue

        video_path = os.path.join(word_path, filename)
        cap = cv2.VideoCapture(video_path)

        left_hand_seq = []
        right_hand_seq = []

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(frame_rgb)

            left_hand = [0.0] * 42
            right_hand = [0.0] * 42

            if results.multi_hand_landmarks:
                for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                    coords = []
                    x_ = [lm.x for lm in hand_landmarks.landmark]
                    y_ = [lm.y for lm in hand_landmarks.landmark]
                    for lm in hand_landmarks.landmark:
                        coords.append(lm.x - min(x_))
                        coords.append(lm.y - min(y_))

                    if handedness.classification[0].label == "Left":
                        left_hand = coords
                    else:
                        right_hand = coords

            left_hand_seq.append(left_hand)
            right_hand_seq.append(right_hand)

        cap.release()

        if len(left_hand_seq) == 0 and len(right_hand_seq) == 0:
            continue

        try:
            left_hand_np = np.array(left_hand_seq)
            right_hand_np = np.array(right_hand_seq)

            combined = np.concatenate([left_hand_np, right_hand_np], axis=1)  # (frames, 84)
            feature_vector = np.mean(combined, axis=0)

            if not np.isnan(feature_vector).any():
                data.append(feature_vector.tolist())
                labels.append(word)
            else:
                print(f"⚠️ Skipped NaN in {filename}")

        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")

# Save dataset
with open('video_communication_data.pickle', 'wb') as f:
    pickle.dump({'data': data, 'labels': labels}, f)

# Summary
print("\n✅ Dataset creation complete!")
print("📊 Class distribution:", Counter(labels))
if data:
    print("🔎 Sample vector (first 10 values):", data[0][:10])
else:
    print("⚠️ No valid samples were found.")
