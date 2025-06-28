import cv2
from PIL import Image, ImageTk
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from inference_classifier_video import extract_landmarks_from_frame, predict_from_sequence, speak, set_voice, landmark_queue

import datetime


# # Remember  you added for imgs + video detection testing right now
# from inference_classifier_video import (
#     extract_landmarks_from_frame,
#     predict_from_sequence,
#     speak,
#     set_voice,
#     landmark_queue
# )

# from inference_classifier_imgs import predict_from_image  # NEW





class SignLanguageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SayAble - Travel & Emergency Assistant")
        self.center_window(1280, 900)
        self.root.resizable(False, False)

        self.theme = "cosmo"
        self.style = ttk.Style(self.theme)

        self.cap = cv2.VideoCapture(0)
        self.prediction_history = []
        self.dark_mode = False
        self.voice_toggle_state = 0

        self.build_ui()
        self.update_video()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def build_ui(self):
        self.frame = ttk.Frame(self.root, padding=20)
        self.frame.pack(fill=BOTH, expand=True)

        header = ttk.Frame(self.frame)
        header.pack(fill=X, pady=10)

        title = ttk.Label(header, text="SayAble - Travel & Emergency Assistant", font=("Helvetica", 24, "bold"), anchor=CENTER)
        title.pack(side=LEFT, padx=10)

        self.theme_toggle = ttk.Button(header, text="\U0001F319 Dark Mode", command=self.toggle_theme, bootstyle="secondary-outline")
        self.theme_toggle.pack(side=RIGHT, padx=10)

        self.voice_toggle = ttk.Button(header, text="\U0001F468 Male Voice", command=self.toggle_voice, bootstyle="info-outline")
        self.voice_toggle.pack(side=RIGHT, padx=10)

        content = ttk.Frame(self.frame)
        content.pack(fill=BOTH, expand=True)

        left_panel = ttk.Frame(content)
        left_panel.pack(side=LEFT, fill=BOTH, expand=True, padx=10)

        self.video_label = ttk.Label(left_panel)
        self.video_label.pack(pady=10, anchor=CENTER)

        self.prediction_label = ttk.Label(left_panel, text="Awaiting gesture input...", font=("Helvetica", 20, "bold"), bootstyle="info")
        self.prediction_label.pack(pady=10)

        self.instructions = ttk.Label(
            left_panel,
            text="Perform a travel or emergency gesture. SayAble will recognize and speak it!",
            font=("Segoe UI", 13, "italic"),
            bootstyle="secondary",
            padding=8
        )
        self.instructions.pack(pady=(0, 10))

        right_panel = ttk.Frame(content)
        right_panel.pack(side=RIGHT, fill=Y, padx=10, pady=10)

        log_frame = ttk.Labelframe(right_panel, text="Interaction Log", padding=10)
        log_frame.pack(fill=BOTH, expand=True, pady=(0, 15))

        self.history_text = tk.Text(log_frame, height=15, font=("Segoe UI", 12), wrap=WORD)
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.history_text.yview)
        self.history_text.config(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=RIGHT, fill=Y)
        self.history_text.pack(side=LEFT, fill=BOTH, expand=True)
        self.history_text.config(state=DISABLED)

        btn_frame = ttk.Frame(right_panel)
        btn_frame.pack(pady=10, fill=X, side=BOTTOM)

        self.speak_again_btn = ttk.Button(btn_frame, text="\U0001F50A Repeat Last Phrase", command=self.speak_last_prediction, bootstyle="success")
        self.speak_again_btn.pack(fill=X, pady=5)

        self.clear_btn = ttk.Button(btn_frame, text="\U0001F9F9 Clear Log", command=self.clear_history, bootstyle="warning")
        self.clear_btn.pack(fill=X, pady=5)

        self.quit_button = ttk.Button(btn_frame, text="\U0001F6AA Exit SayAble", command=self.quit_app, bootstyle="danger")
        self.quit_button.pack(fill=X, pady=5)

    def update_video(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            landmarks = extract_landmarks_from_frame(frame)
            landmark_queue.append(landmarks)

            prediction = predict_from_sequence()

            if prediction:
                display_prediction = prediction.capitalize()
                self.prediction_label.config(text=f"Detected: {display_prediction}")
                self.log_prediction(display_prediction)
            else:
                self.prediction_label.config(text="Awaiting gesture input...")

            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)

        self.root.after(10, self.update_video)



    # def update_video(self):
    #     ret, frame = self.cap.read()
    #     if ret:
    #         frame = cv2.flip(frame, 1)

    #     # Step 1: Run video model prediction
    #         landmarks = extract_landmarks_from_frame(frame)
    #         landmark_queue.append(landmarks)
    #         video_prediction = predict_from_sequence()

    #         final_prediction = None

    #         if video_prediction:
    #             final_prediction = video_prediction
    #         else:
    #         # Step 2: Try fallback static image-based prediction
    #             image_prediction = predict_from_image(frame)
    #             if image_prediction:
    #                 final_prediction = image_prediction

    #     # Step 3: Display prediction
    #         if final_prediction:
    #             display_prediction = final_prediction.capitalize()
    #             self.prediction_label.config(text=f"Detected: {display_prediction}")
    #             self.log_prediction(display_prediction)
    #         else:
    #             self.prediction_label.config(text="Awaiting gesture input...")

    #     # Step 4: Show webcam frame
    #         img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    #         img = Image.fromarray(img)
    #         imgtk = ImageTk.PhotoImage(image=img)
    #         self.video_label.imgtk = imgtk
    #         self.video_label.configure(image=imgtk)

    #     self.root.after(10, self.update_video)


    def log_prediction(self, text):
        if not self.prediction_history or self.prediction_history[-1] != text:
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            entry = f"[{timestamp}] {text}\n"
            self.prediction_history.append(text)
            self.history_text.config(state=tk.NORMAL)
            self.history_text.insert(tk.END, entry)
            self.history_text.see(tk.END)
            self.history_text.config(state=tk.DISABLED)

    def speak_last_prediction(self):
        if self.prediction_history:
            speak(self.prediction_history[-1])

    def clear_history(self):
        self.prediction_history.clear()
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        self.history_text.config(state=tk.DISABLED)

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        new_theme = "darkly" if self.dark_mode else "cosmo"
        self.style.theme_use(new_theme)
        self.theme_toggle.config(text="\u2600\ufe0f Light Mode" if self.dark_mode else "\U0001F319 Dark Mode")

    def toggle_voice(self):
        self.voice_toggle_state = 1 - self.voice_toggle_state
        set_voice(self.voice_toggle_state)
        new_label = "\U0001F469 Female Voice" if self.voice_toggle_state else "\U0001F468 Male Voice"
        self.voice_toggle.config(text=new_label)

    def quit_app(self):
        self.cap.release()
        self.root.destroy()

if __name__ == "__main__":
    root = ttk.Window(themename="cosmo")
    app = SignLanguageApp(root)
    root.mainloop()


