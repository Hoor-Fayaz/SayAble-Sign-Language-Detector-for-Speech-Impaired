import pickle
import numpy as np
import mediapipe as mp
import pyttsx3
import threading
import cv2
from collections import deque

# === Load Model ===
model_dict = pickle.load(open('./video_communication_model.p', 'rb'))
model = model_dict['model']
word_classes = model_dict['classes']

# === MediaPipe Hands ===
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# === Text-to-Speech ===
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')
current_voice_index = 0
engine.setProperty('voice', voices[current_voice_index].id)

# Voice Setter
def set_voice(index):
    global current_voice_index
    if 0 <= index < len(voices):
        current_voice_index = index
        engine.setProperty('voice', voices[current_voice_index].id)

# Safe speak to prevent RuntimeError
is_speaking = False

def speak(text):
    global is_speaking
    if is_speaking:
        return
    is_speaking = True
    threading.Thread(target=_speak_thread, args=(text,), daemon=True).start()

def _speak_thread(text):
    global is_speaking
    try:
        engine.setProperty('voice', voices[current_voice_index].id)
        engine.say(text)
        engine.runAndWait()
    except RuntimeError:
        pass
    is_speaking = False

# === Landmark Extraction ===
def extract_landmarks_from_frame(frame):
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    left_hand = [0.0] * 42
    right_hand = [0.0] * 42

    if results.multi_hand_landmarks:
        for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            coords = []
            x_vals = [lm.x for lm in hand_landmarks.landmark]
            y_vals = [lm.y for lm in hand_landmarks.landmark]
            for lm in hand_landmarks.landmark:
                coords.append(lm.x - min(x_vals))
                coords.append(lm.y - min(y_vals))
            if handedness.classification[0].label == "Left":
                left_hand = coords
            else:
                right_hand = coords

    return left_hand + right_hand  # (84,)

# === Inference Setup ===
sequence_length = 20
landmark_queue = deque(maxlen=sequence_length)

previous_prediction = None
prediction_count = 0
confirmed_prediction = None
required_consistency = 5
confidence_threshold = 0.4

# === Inference Function ===
def predict_from_sequence():
    global previous_prediction, prediction_count, confirmed_prediction

    if len(landmark_queue) < sequence_length:
        return None

    sequence_np = np.array(landmark_queue)
    feature_vector = np.mean(sequence_np, axis=0).reshape(1, -1)

    try:
        proba = model.predict_proba(feature_vector)[0]
        max_confidence = np.max(proba)
        prediction = model.classes_[np.argmax(proba)]
    except AttributeError:
        # fallback if model doesn’t support predict_proba
        prediction = model.predict(feature_vector)[0]
        max_confidence = 1.0

    print(f"🧠 Predicted: {prediction} | 🔢 Confidence: {max_confidence:.2f}")

    # Ignore low-confidence predictions
    if max_confidence < confidence_threshold:
        return None

    # Stability logic
    if prediction == previous_prediction:
        prediction_count += 1
    else:
        prediction_count = 1
        previous_prediction = prediction

    if prediction_count >= required_consistency:
        if confirmed_prediction != prediction:
            confirmed_prediction = prediction
            speak(confirmed_prediction)
        return confirmed_prediction

    return None
