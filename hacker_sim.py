# hacker_sim.py

import time
import os
import random

STOP_FILE = "stop.txt"

def slow_print(text, delay=0.03):
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()

slow_print("Initializing system...\n", 0.05)

while True:
    # stop check
    if os.path.exists(STOP_FILE):
        with open(STOP_FILE, "r") as f:
            if f.read().strip()  == "STOP":
                slow_print("\n[!] External override detected...")
                slow_print("Shutting down simulation...\n", 0.05)
                break

    # Fake "matrix-like" output
    line = "".join(random.choice("01ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(40))
    print("\033[92m" + line + "\033[0m") # green text
    time.sleep(0.1)
          
    
