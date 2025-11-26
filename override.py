# override.py

import time

with open("stop.txt", "w") as f:
    f.write("STOP")

print("[Override] Shutdown command sent.")
time.sleep(1)
