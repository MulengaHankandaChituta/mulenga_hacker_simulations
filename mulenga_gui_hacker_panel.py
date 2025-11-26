# GUI Hacker Panel (Tkinter)
# mulenga_gui_hacker_panel.py
# Start/Stop controls, visual-only fake brute force.
# Quit normally with window close. The stop button halts the simulation

import tkinter as tk
import threading
import random
import time
import os

STOP_FILE = "stop.txt"

class HackerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hacker Panel (Simulation)")
        self.geometry("900x600")
        self.running = False
        self.create_widgets()

    def create_widgets(self):
        self.top_frame = tk.Frame(self, height=350)
        self.top_frame.pack(fill="both", expand=False)

        self.canvas = tk.Canvas(self.top_frame, bg="black")
        self.canvas.pack(fill="both", expand=True)

        self.bottom_frame = tk.Frame(self, height=250)
        self.bottom_frame.pack(fill="x", side="bottom")

        # controls
        self.start_btn = tk.Button(self.bottom_frame, text="Start", command=self.start)
        self.start_btn.pack(side="left", padx=10, pady=10)
        self.stop_btn = tk.Button(self.bottom_frame, text="Stop", command=self.stop)
        self.stop_btn.pack(side="left", padx=10, pady=10)

        self.brute_label = tk.Label(self.bottom_frame, text="Fake Target:")
        self.brute_label.pack(side="left", padx=0)
        self.target_entry = tk.Entry(self.bottom_frame)
        self.target_entry.pack(side="left", padx=6)
        self.target_entry.insert(0, "example.local")

        self.brute_btn = tk.Button(self.bottom_frame, text="Start Fake Brute", command=self.start_bruteforce)
        self.brute_btn.pack(side="left", padx=6)

        self.log = tk.Text(self.bottom_frame, height=6, width=50)
        self.log.pack(side="right", padx=10)

        # for matrix effect
        self.drops = []
        self.after_id = None

    def start(self):
        if not self.running:
            self.running = True
            self.log_insert("[GUI] Simulation started.")
            self.animate_matrix()

    def stop(self):
        if self.running:
            self.running = False
            self.log_insert("[GUI] Simulation stopped.")
        # allow external STOP file to also stop threads
        if os.path.exists(STOP_FILE):
            try:
                with open(STOP_FILE, "r") as f:
                    if f.read().strip() == "STOP":
                        self.running = False
                        self.log_insert("[GUI] External STOP flag detected.")
            except Exception as e:
                self.log_insert(f"[GUI] Error reading STOP file: {e}")

    def log_insert(self, msg):
        ts = time.strftime("%H:%M:%S")
        self.log.insert("end", f"[{ts}] {msg}\n")
        self.log.see("end")

    def animate_matrix(self):
        if not self.running:
            if self.after_id:
                self.after_cancel(self.after_id)
            return
        
        w = self.canvas.winfo_width() or 900
        h = self.canvas.winfo_height() or 350

        self.canvas.delete("all")
        columns = w // 10
        for c in range(columns):
            if random.random() < 0.02:
                x = c * 10
                y = random.randint(-h, 0)
                length = random.randint(5, 20)
                for i in range(length):
                    char = random.choice('01abcdefghijklmnopqrstuvwxyz')
                    self.canvas.create_text(x, y + i*12, text=char, fill="#00FF00", anchor="nw", font=("Consoles", 10))

        # schedule next frame
        self.after_id = self.after(80, self.animate_matrix)

    def start_bruteforce(self):
        target = self.target_entry.get().strip() or "example.local"
        self.log_insert(f"[BRUTE] Starting fake brute against {target}")
        t = threading.Thread(target=self.fake_bruteforce,  args=(target,), daemon=True)
        t.start()

    def fake_bruteforce(self, target):
        attempts = 0
        while attempts < 1000 and (self.running or True):
            # external stop check
            if os.path.exists(STOP_FILE):
                with open(STOP_FILE, "r") as f:
                    if f.read().strip() == "STOP":
                        self.log_insert("[BRUTE] External STOP detected. Ending fake brute.")
                        return
                    
            attempts += 1
            guess = "".join(random.choice("abcdefghijklmnopqrstuvwxyz0123456789") for _ in range(random.randint(6,12)))
            self.log_insert(f"[BRUTE] {attempts:04d} -> {guess}")
            time.sleep(random.uniform(0.01, 0.12))

            # occasionally show a fake match animation then continue
            if random.random() < 0.0015:
                self.log_insert("[BRUTE] Partial collision (simulated).  Continuing...")

        self.log_insert("[BRUTE] Fake brute finished (simulated).")

if __name__ == "__main__":
    app = HackerGUI()
    app.mainloop()

