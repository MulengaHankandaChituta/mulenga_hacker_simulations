# matrix_rain.py
# Full-screen matrix rain effect using curses
# Quit: press "q" or create a file call "stop.txt" containing STOP

import curses
import random
import time

def main(stdscr):
    curses.curs_set(0)            # Hide cursor
    stdscr.nodelay(True)          # Non-blocking input
    stdscr.clear()

    sh, sw = stdscr.getmaxyx()
    columns = [0] * sw

    chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    while True:
        # Quit with 'q'
        key = stdscr.getch()
        if key == ord('q'):
            break

        stdscr.erase()

        for i in range(sw):
            if random.random() < 0.02:
                columns[i] = random.randint(1, sh - 1)

            if columns[i] > 0:
                try:
                    # Draw bright head
                    stdscr.addstr(columns[i], i, random.choice(chars), curses.A_BOLD)
                except curses.error:
                    pass

                # Draw tail
                for j in range(1, 5):
                    y = columns[i] - j
                    if 0 <= y < sh:
                        try:
                            stdscr.addstr(y, i, random.choice(chars))
                        except curses.error:
                            pass

                columns[i] += 1
                if columns[i] >= sh:
                    columns[i] = 0

        stdscr.refresh()
        time.sleep(0.05)

if __name__ == "__main__":
    curses.wrapper(main)
