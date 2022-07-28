#!/usr/bin/env python3

'''
Cardiac Coherence breathing exercise from the comfort of your Unix terminal.

Feeling stressed out? Say no more!
Start breathe.py and follow along.

Breathe in calmly and evenly as the marker sweeps the terminal from the left
to the right, breathe out as the marker comes back to the left hand side.
Repeat. A five minute session will have a long lasting calming effect.
'''

from itertools import chain
import math
import re
import shutil
import signal
import sys
import termios
import time

def print_code(code):
    '''Print ANSI escape code'''
    print(code, end='', flush=True)


def show_cursor(show=True):
    '''Show or hide the cursor'''
    print_code("\033[?25h" if show else "\033[?25l")


def get_cursor_position():
    '''
    Get the current cursor position.
    From: https://stackoverflow.com/questions/35526014
    '''
    old_mode = termios.tcgetattr(sys.stdin)
    mode = termios.tcgetattr(sys.stdin)
    mode[3] = mode[3] & ~(termios.ECHO | termios.ICANON)
    termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, mode)

    try:
        print_code("\033[6n")
        ans = ""
        while True:
            ans += sys.stdin.read(1)
            if ans.endswith('R'):
                break
        res = re.match(r".*\[(?P<y>\d*);(?P<x>\d*)R", ans)
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, old_mode)

    if (res):
        return (res.group("x"), res.group("y"))
    return (0, 0)


def move_to(x, y):
    '''Move the cursor to given position'''
    print_code(f"\033[{y};{x}H")


def erase_line():
    '''Erase the current line'''
    print_code("\r\033[K")

def restore_term(sig, frame):
    '''Cleanup state'''
    erase_line()
    show_cursor()
    sys.exit(0)


# cursor_col = 0.5 * cols_nr * (1 - cos(π * (t - t0) / Δt))
# t = t0 + Δt * acos(1 - 2 * cursor_col / cols_nr) / π
def time_at_pos(cols, dur, i, offset=0.0):
    '''
    Compute the time delay to reach column i for a sine wave of total duration dur
    to span a terminal width of cols columns.
    '''
    return offset + dur * math.acos(1.0 - 2.0 * i / cols) / math.pi

def breathe_cycle(in_duration, out_duration):
    '''
    Perform a breathing cycle of total duration in_duration + out_duration.
    Inhale for in_duration seconds as the marker on the screen sweeps the
    terminal from the left hand side to the right hand side, then exhale for
    out_duration seconds as the marker comes back to the left hand side.
    The marker moves in a sine wave, which I find more natural.
    '''
    cols, _ = shutil.get_terminal_size()
    _, y = get_cursor_position()

    rg = range(1, cols + 1)
    # positions for the first half of a cycle
    d_in = [time_at_pos(cols, in_duration, ind, 0) for ind in rg]
    # positions for the second half of a cycle
    d_out = [time_at_pos(cols, out_duration, ind, in_duration) for ind in rg]

    # positions and times for a full cycle
    cycle_x_positions = chain(rg, reversed(rg))
    cycle_times = chain(d_in, d_out)

    d0 = time.monotonic_ns()
    for x, t in zip(cycle_x_positions, cycle_times):
        move_to(x, y)
        print_code("*")
        dt = (d0 + t * 1.0e9 - time.monotonic_ns()) / 1.0e9
        time.sleep(abs(dt))
        move_to(x, y)
        print_code(" ")


def main():
    '''Perform breathing cycles until Crtl+C occurs'''
    if not sys.stdin.isatty():
        sys.exit(1)

    import argparse
    parser = argparse.ArgumentParser(
        description='Cardiac Coherence breathing exercise from the comfort of your Unix terminal.'
    )
    parser.add_argument('-i', type=float, default=5.5, help='breathe in duration in seconds', dest='in_duration')
    parser.add_argument('-o', type=float, default=5.5, help='breathe out duration in seconds', dest='out_duration')
    parser.add_argument('-t', type=float, default=2.0, help='Session duration in minutes', dest='session_duration')
    args = parser.parse_args()

    show_cursor(False)
    signal.signal(signal.SIGINT, restore_term)
    t0 = time.time()
    while (time.time() - t0) <= args.session_duration * 60:
        breathe_cycle(args.in_duration, args.out_duration)
    print("Session finished !")
    show_cursor(True)


if __name__ == '__main__':
    main()
