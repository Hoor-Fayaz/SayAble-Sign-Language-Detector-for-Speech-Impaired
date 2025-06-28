


# # inference_classifier.py

import pickle
import numpy as np
import mediapipe as mp
import pyttsx3
import threading
import cv2

# Load model
model = pickle.load(open('./model.p', 'rb'))['model']

# MediaPipe setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1,
                       min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Text-to-speech
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

voices = engine.getProperty('voices')
current_voice_index = 0  # 0 for male (typically), 1 for female

def set_voice(index):
    global current_voice_index
    current_voice_index = index
    if 0 <= index < len(voices):
        engine.setProperty('voice', voices[index].id)

# Set default voice
set_voice(current_voice_index)

# Stability check vars
previous_prediction = None
prediction_count = 0
required_consistency = 7
confirmed_prediction = None

def speak(text):
    threading.Thread(target=lambda: _speak_thread(text), daemon=True).start()

def _speak_thread(text):
    engine.setProperty('voice', voices[current_voice_index].id)
    engine.say(text)
    engine.runAndWait()

def predict_and_speak_from_frame(frame):
    global previous_prediction, prediction_count, confirmed_prediction

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    H, W, _ = frame.shape
    data_aux = []
    x_, y_ = [], []

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for lm in hand_landmarks.landmark:
                x_.append(lm.x)
                y_.append(lm.y)

            for lm in hand_landmarks.landmark:
                data_aux.append(lm.x - min(x_))
                data_aux.append(lm.y - min(y_))

            # Prediction
            prediction = model.predict([np.asarray(data_aux)])
            predicted_character = prediction[0]

            if predicted_character == previous_prediction:
                prediction_count += 1
            else:
                prediction_count = 1
                previous_prediction = predicted_character

            if prediction_count == required_consistency:
                if confirmed_prediction != predicted_character:
                    confirmed_prediction = predicted_character
                    speak(confirmed_prediction)

            return confirmed_prediction  # For GUI display

    else:
        previous_prediction = None
        prediction_count = 0
        confirmed_prediction = None

    return None
