# # inference_classifier.py (for digits 0–9)
# import pickle
# import numpy as np
# import mediapipe as mp
# import pyttsx3
# import threading
# import cv2

# # Load digit model
# model = pickle.load(open('./digit_model.p', 'rb'))['model']

# # MediaPipe setup
# mp_hands = mp.solutions.hands
# mp_drawing = mp.solutions.drawing_utils
# hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1,
#                        min_detection_confidence=0.5, min_tracking_confidence=0.5)

# # Text-to-speech
# engine = pyttsx3.init()
# engine.setProperty('rate', 150)
# engine.setProperty('volume', 1.0)

# # Stability check variables
# previous_prediction = None
# prediction_count = 0
# required_consistency = 7
# confirmed_prediction = None


# def speak(text):
#     threading.Thread(target=lambda: engine.say(text) or engine.runAndWait(), daemon=True).start()


# def predict_and_speak_from_frame(frame):
#     global previous_prediction, prediction_count, confirmed_prediction

#     frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#     results = hands.process(frame_rgb)

#     H, W, _ = frame.shape
#     data_aux = []
#     x_, y_ = [], []

#     if results.multi_hand_landmarks:
#         for hand_landmarks in results.multi_hand_landmarks:
#             for lm in hand_landmarks.landmark:
#                 x_.append(lm.x)
#                 y_.append(lm.y)

#             for lm in hand_landmarks.landmark:
#                 data_aux.append(lm.x - min(x_))
#                 data_aux.append(lm.y - min(y_))

#             # Model prediction
#             prediction = model.predict([np.asarray(data_aux)])
#             predicted_digit = prediction[0]

#             # Stability check
#             if predicted_digit == previous_prediction:
#                 prediction_count += 1
#             else:
#                 prediction_count = 1
#                 previous_prediction = predicted_digit

#             if prediction_count == required_consistency:
#                 if confirmed_prediction != predicted_digit:
#                     confirmed_prediction = predicted_digit
#                     speak(str(confirmed_prediction))

#             return confirmed_prediction  # For UI even if unconfirmed

#     else:
#         # Reset if no hand
#         previous_prediction = None
#         prediction_count = 0
#         confirmed_prediction = None

#     return None



import pickle
import numpy as np
import mediapipe as mp
import pyttsx3
import threading
import cv2

# Load digit model
model = pickle.load(open('./digit_model.p', 'rb'))['model']

# MediaPipe setup
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1,
                       min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Text-to-speech
engine = pyttsx3.init()
engine.setProperty('rate', 150)
engine.setProperty('volume', 1.0)

# Set default voice to male (0 = male, 1 = female)
voice_gender = 0
voices = engine.getProperty('voices')

def set_voice(gender: int):
    global voice_gender
    voice_gender = gender
    engine.setProperty('voice', voices[gender].id)

# Stability check variables
previous_prediction = None
prediction_count = 0
required_consistency = 7
confirmed_prediction = None


def speak(text):
    threading.Thread(
        target=lambda: (
            engine.setProperty('voice', voices[voice_gender].id),
            engine.say(text),
            engine.runAndWait()
        ),
        daemon=True
    ).start()


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

            # Model prediction
            prediction = model.predict([np.asarray(data_aux)])
            predicted_digit = prediction[0]

            # Stability check
            if predicted_digit == previous_prediction:
                prediction_count += 1
            else:
                prediction_count = 1
                previous_prediction = predicted_digit

            if prediction_count == required_consistency:
                if confirmed_prediction != predicted_digit:
                    confirmed_prediction = predicted_digit
                    speak(str(confirmed_prediction))

            return confirmed_prediction  # For UI even if unconfirmed

    else:
        # Reset if no hand
        previous_prediction = None
        prediction_count = 0
        confirmed_prediction = None

    return None
