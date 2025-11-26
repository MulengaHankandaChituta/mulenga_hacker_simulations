# retro hacker with a user interface
# retro_hacker_ui.py
# Retro hacker-styled terminal UI using curses
# Keys: s=start simulation, x=stop simulation, q=quit
# also honors stop.txt containing stop

import curses
import time
import threading
import random
import os

STOP_FILE = "stop.txt"
running = False
log_lines = []

def fake_worker():
    global running, log_lines
    counter = 0
    while running:
        if os.path.exists(STOP_FILE):
            with open(STOP_FILE, "r") as f:
                if f.read().strip() == "STOP":
                    log_lines.append("[SYSTEM] External STOP flag detexted.")
                    running = False
                    break

                counter += 1
                log_lines.append(f"[{time.strftime('%H:%M:%S')}] evt#{counter} - {random.choice(['INIT', 'HOOK', 'SCAN', 'PROBE', 'ECHO'])}")

                # keep log size reasonable

                if len(log_lines) > 200:
                    log_lines = log_lines[-200:]
                time.sleep(random.uniform(0.2, 0.6))

def draw_ui(stdscr):
    curses.curs_set(0)
    sh, sw = stdscr.getmaxyx()

    # widows sizes

    log_h = int(sh * 0.6)
    stat_h = sh - log_h - 3

    log_win = curses.newwin(log_h, sw, 0, 0)
    stat_win = curses.newwin(stat_h, sw//2, log_h, 0)
    cmd_win = curses.newwin(stat_h, sw - sw//2, log_h, sw//2)
    hint_win = curses.newwin(3, sw, sh-3, 0)

    stdscr.nodelay(True)
    stdscr.timeout(100)

    worker_thread = None
    global running

    while True:
        # stop flag
        if os.path.exists(STOP_FILE):
            with open(STOP_FILE, "r") as f:
                if f.read().strip() == "STOP":
                    running = False

        ch = stdscr.getch()
        if ch == ord('q'):
            running = False
            break
        elif ch == ord('s'):
            if not running:
                running = True
                log_lines.append("[SYSTEM] Simulation started.")
                worker_thread = threading.Thread(target=fake_worker, daemon=True)
                worker_thread.start()
        elif ch == ord('x'):
            if running:
                running = False
                log_lines.append("[SYSTEM] Simulation stopping...")

        # draw log window
        log_win.erase()
        log_win.box()
        log_win.addstr(0, 2, " LOG ")
        to_show = log_lines[-(log_h-2):]
        for i, line in enumerate(to_show):
            try:
                log_win.addstr(1+i, 1, line[:sw-2])
            except curses.error:
                pass

        # stat window
        stat_win.erase()
        stat_win.box()
        stat_win.addstr(0, 2, " SYSTEM ")
        cpu = random.uniform(1, 99)
        mem = random.uniform(1, 99)
        stat_win.addstr(1, 2, f"CPU: {cpu:.2f}%")
        stat_win.addstr(2, 2, f"MEM: {mem:.2f}%")
        stat_win.addstr(3, 2, f"Threads: {random.randint(1,12)}")
        stat_win.addstr(4, 2, f"Uptime: {int(time.time())%99999}s")

        # command window
        cmd_win.erase()
        cmd_win.box()
        cmd_win.addstr(0, 2, " CONSOLE ")
        cmd_win.addstr(1, 2, "Press 's' to start, 'x' to stop, 'q' to quit.")
        if running:
            cmd_win.addstr(3, 2, "STATUS RUNNING")
        else:
            cmd_win.addstr(3, 2, "STATUS: IDLE")

        # hint window
        hint_win.erase()
        hint_win.addstr(0, 1, "Retro Hacker UI -  purely visual. This does not access networks or systems.")
        hint_win.addstr(1, 1, "Create stop.txt with STOP to request an external stop.")
        hint_win.addstr(2, 1, f"Logs: {len(log_lines)}")

        # refresh all
        log_win.refresh()
        stat_win.refresh()
        cmd_win.refresh()
        hint_win.refresh()

        time.sleep(0.1)

if __name__ == "__main__":
    try:
        curses.wrapper(draw_ui)
    except KeyboardInterrupt:
        pass


