# Fake password Brute-Forcer(visual only)
# fake_bruteforce.py
# Visual only fake password brute forcer
# Enter a made-up "target" name and watch the pretend attempts
# Quit: press Ctrl+c or create a file named "stop.txt" containg STOP

import time
import random
import string
import os

STOP_FILE = "stop.txt"

def gen_guess(length=8):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return "".join(random.choice(chars) for _ in range(length))

def main():
    target = input("Enter target (fake): ").strip() or "192.168.0.1"
    print(f"Starting visual brute force against {target} (simulation).")
    print("Press Ctrl+c to stop or create 'stop.txt' with STOP.\n")

    attempts = 0
    try:
        while True:
            # stop flag
            if os.path.exists(STOP_FILE):
                with open(STOP_FILE, "r") as f:
                    if f.read().strip() == "STOP":
                        print("\n[!] External STOP detected. Ending simulation.")
                        break

            attempts += 1
            guess = gen_guess(random.randint(6, 12))
            latency = random.uniform(0.02, 0.25)
            # show tries faster at first, slow later
            print(f"[{attempts:06d}] Trying: {guess} -> latency {latency:.3f}s", end="\r")
            time.sleep(latency)

            # occasional fake "match" animation but never reveals real credentials

            if random.random() < 0.0006:
                print()
                for s in ["Cracking", "Bypassing", "Decrypting", "Injecting"]:
                    print(f"{s} .", end="\r")
                    time.sleep(0.4)
                outcome = random.choice(["ACCESS DENIED", "ACCESS GRANTED (SIMULATED)"])
                print(f"\n>>> {outcome} (simulation only)")
                time.sleep(1.5)

                # continue simulation
                print("Resuming simulation...\n")

    except  KeyboardInterrupt:
        print("\nInterrupted by user. Exiting.")

if __name__ == "__main__":
    main()
                
                
