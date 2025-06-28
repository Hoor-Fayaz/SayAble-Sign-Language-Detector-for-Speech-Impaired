import subprocess
import os
import sys
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class MainLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("SayAble - Sign Language Recognition Launcher")
        self.project_root = os.path.dirname(os.path.abspath(__file__))

        icon_path = os.path.join(self.project_root, "assets", "SayAble_Logo.ico")
        self.root.iconbitmap(icon_path)

        self.center_window(1280, 900)
        self.root.resizable(False, False)

        self.style = ttk.Style("darkly")  # Set default theme to darkly
        self.dark_mode = True

        # Define styles for labels
        self.style.configure("Dark.TLabel", background="#121212", foreground="white", font=("Helvetica", 14))
        self.style.configure("Light.TLabel", background="white", foreground="black", font=("Helvetica", 14))

        self.build_ui()

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def build_ui(self):
        # Create a scrollable canvas
        canvas = tk.Canvas(self.root, borderwidth=0, highlightthickness=0)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Add inner frame to canvas
        self.frame = ttk.Frame(canvas, padding=40)
        self.canvas_window = canvas.create_window((0, 0), window=self.frame, anchor="n")

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def on_canvas_resize(event):
            canvas.itemconfig(self.canvas_window, width=event.width)

        self.frame.bind("<Configure>", on_frame_configure)
        canvas.bind("<Configure>", on_canvas_resize)

        # Load content inside scrollable frame
        self.load_logo_and_content()

    def load_logo_and_content(self):
        logo_path = os.path.join(self.project_root, "assets", "SayAble_Logo.png")

        if os.path.exists(logo_path):
            logo_img = tk.PhotoImage(file=logo_path)
            self.logo = ttk.Label(self.frame, image=logo_img)
            self.logo.image = logo_img
            self.logo.pack(pady=(10, 20))
        else:
            self.logo = ttk.Label(
                self.frame,
                text="Logo Missing",
                style="Dark.TLabel" if self.dark_mode else "Light.TLabel"
            )
            self.logo.pack(pady=(10, 20))

        self.title_label = ttk.Label(
            self.frame,
            text="SayAble - Gesture-Based Personal Assistant",
            style="Dark.TLabel" if self.dark_mode else "Light.TLabel",
            font=("Helvetica", 28, "bold"),
            anchor="center"
        )
        self.title_label.pack(pady=10)

        desc = (
            "Welcome to SayAble!\n\n"
            "This AI-powered tool helps people with speech impairments communicate through gestures.\n"
            "Use the webcam to show ASL signs and SayAble will speak them aloud.\n\n"
            "➤ Use Alphabet Mode for letter-based spelling and phrases.\n"
            "➤ Use Number Mode to show numeric signs.\n"
            "➤ Use Travel & Emergency Mode for travel and emergency-related gesture words.\n"
            "➤ Use Greetings & Communication Mode for common conversational words.\n"
            "➤ Use Food & Shopping Mode for food ordering and shopping-related gesture words.\n"
        )

        self.description_label = ttk.Label(
            self.frame,
            text=desc,
            style="Dark.TLabel" if self.dark_mode else "Light.TLabel",
            font=("Segoe UI", 14),
            wraplength=1000,
            justify="left"
        )
        self.description_label.pack(pady=10)

        # --- Alphabet & Number (Non-word-level) ---
        nonword_frame = ttk.Frame(self.frame)
        nonword_frame.pack(pady=(30, 10))

        alphabet_btn = ttk.Button(
            nonword_frame, text="🅰️  Alphabet Mode", command=self.launch_alphabet,
            width=25, bootstyle="primary"
        )
        alphabet_btn.grid(row=0, column=0, padx=20, pady=15, sticky="ew")

        number_btn = ttk.Button(
            nonword_frame, text="🔢  Number Mode", command=self.launch_number,
            width=25, bootstyle="info"
        )
        number_btn.grid(row=0, column=1, padx=20, pady=15, sticky="ew")

        for i in range(2):
            nonword_frame.grid_columnconfigure(i, weight=1)

        # --- Word-level Modes ---
        word_frame = ttk.Frame(self.frame)
        word_frame.pack(pady=(10, 30))

        travel_btn = ttk.Button(
            word_frame, text="🧳 Travel & Emergency Mode", command=self.launch_travel,
            width=30, bootstyle="warning"
        )
        travel_btn.grid(row=0, column=0, padx=20, pady=15, sticky="ew")

        greetings_btn = ttk.Button(
            word_frame, text="💬 Greetings & Communication Mode", command=self.launch_greetings,
            width=35, bootstyle="success"
        )
        greetings_btn.grid(row=0, column=1, padx=20, pady=15, sticky="ew")

        food_btn = ttk.Button(
            word_frame, text="🍔 Food & Shopping Mode", command=self.launch_food,
            width=32, bootstyle="danger"
        )
        food_btn.grid(row=0, column=2, padx=20, pady=15, sticky="ew")

        for i in range(3):
            word_frame.grid_columnconfigure(i, weight=1)

        # --- (Future) Sentence-level Modes ---
        # sentence_frame = ttk.Frame(self.frame)
        # sentence_frame.pack(pady=(10, 30))
        # Add your sentence-level buttons here

        self.theme_toggle = ttk.Button(
            self.frame, text="☀️ Light Mode", command=self.toggle_theme,
            bootstyle="secondary-outline"
        )
        self.theme_toggle.pack(pady=10)

        self.apply_theme_styles()

    def launch_alphabet(self):
        alphabet_path = os.path.join(self.project_root, "AlphabetDetection", "gui_app.py")
        if not os.path.exists(alphabet_path):
            print(f"Error: {alphabet_path} not found!")
            return
        subprocess.Popen([sys.executable, alphabet_path])

    def launch_number(self):
        number_path = os.path.join(self.project_root, "NumberDetection", "gui_app.py")
        if not os.path.exists(number_path):
            print(f"Error: {number_path} not found!")
            return
        subprocess.Popen([sys.executable, number_path])

    def launch_travel(self):
        travel_path = os.path.join(self.project_root, "Travel&Emergency", "guiapp_video.py")
        if not os.path.exists(travel_path):
            print(f"Error: {travel_path} not found!")
            return
        subprocess.Popen([sys.executable, travel_path])

    def launch_greetings(self):
        greetings_path = os.path.join(self.project_root, "Greetings&Communication", "guiapp_video.py")
        if not os.path.exists(greetings_path):
            print(f"Error: {greetings_path} not found!")
            return
        subprocess.Popen([sys.executable, greetings_path])

    def launch_food(self):
        food_path = os.path.join(self.project_root, "Food&Shopping", "guiapp_video.py")
        if not os.path.exists(food_path):
            print(f"Error: {food_path} not found!")
            return
        subprocess.Popen([sys.executable, food_path])

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        theme = "darkly" if self.dark_mode else "cosmo"
        self.style.theme_use(theme)

        label_style = "Dark.TLabel" if self.dark_mode else "Light.TLabel"
        self.title_label.config(style=label_style)
        self.description_label.config(style=label_style)
        if hasattr(self.logo, "config"):
            self.logo.config(style=label_style)

        self.theme_toggle.config(text="☀️ Light Mode" if self.dark_mode else "🌙 Dark Mode")

        self.apply_theme_styles()

    def apply_theme_styles(self):
        bg_color = "#121212" if self.dark_mode else "#ffffff"
        self.root.configure(background=bg_color)
        self.frame.configure(style="TFrame")
        for widget in self.root.winfo_children():
            try:
                widget.configure(background=bg_color)
            except:
                pass

if __name__ == "__main__":
    root = ttk.Window(themename="darkly")  # Start with dark theme
    app = MainLauncher(root)
    root.mainloop()