# SayAble: Sign Language Detector

SayAble is an AI-powered Sign Language Detector designed to assist speech-impaired individuals in communicating more effectively. The application leverages computer vision and machine learning to recognize sign language gestures via webcam and translates them into spoken words or phrases.

---

## Features

- **Alphabet Detection:**  
  Recognizes American Sign Language (ASL) alphabets using a webcam. Useful for spelling names or words letter by letter.

- **Number Detection:**  
  Detects numeric signs (0-9) in ASL, enabling users to communicate numbers easily especially contact numbers.

- **Word-Level Recognition:**  
  Identifies a set of common words related to daily communication, travel, emergencies, greetings, food, and shopping.

- **User-Friendly Dashboard:**  
  The main interface (`main_window.py`) provides a dashboard with buttons to launch each specialized model.

---

## Project Structure

- `main_window.py`  
  Main user interface/dashboard. Allows users to select and launch different recognition modules.

- `AlphabetDetection/`  
  Contains code and models for alphabet recognition.

- `NumberDetection/`  
  Contains code and models for number recognition.

- `Travel&Emergency/`  
  Word-level detection for travel and emergency-related gestures.

- `Greetings&Communication/`  
  Word-level detection for greetings and everyday communication.

- `Food&Shopping/`  
  Word-level detection for food and shopping-related gestures.

---

## How to Use

1. **Run `main_window.py`**  
   Launch the dashboard and select the desired recognition mode.

2. **Choose a Mode:**  
   - Alphabet, Number, Travel & Emergency, Greetings & Communication, or Food & Shopping.

3. **Perform Gestures:**  
   Use your webcam to perform the relevant sign language gesture. The system will recognize and display (and optionally speak) the detected word or phrase.

4. **View Output:**  
   The recognized word will appear on the screen. The system will also speak the output.

---

## Requirements

- Python 3.8+
- OpenCV
- Mediapipe
- scikit-learn
- ttkbootstrap
- Pillow
- pyttsx3



---

## Notes

- **Sentence-Level Recognition:**  
  Experimental and under development. The current version supports only word-level detection for reliability and speed.

- **Dataset:**  
  Custom datasets were recorded for each mode.

---

## Credits

Developed by Hoor Fayaz as a university project for assisting speech-impaired individuals using AI and computer vision.

---
