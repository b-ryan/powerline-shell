#!/usr/bin/env python2
from __future__ import print_function

import sys

ESCAPE = chr(27)

def fg(color):
    return ESCAPE + '[38;5;{0}m'.format(color)

def bg(color):
    return ESCAPE + '[48;5;{0}m'.format(color)

def reset():
    return ESCAPE + '[48;0m'

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print('Usage: colortest.py fg_start fg_end bg_start bg_end test_string')
        sys.exit(1)

    fg_start, fg_end, bg_start, bg_end = map(int, sys.argv[1:5])
    test_string = sys.argv[5]

    print(' ' * len(str(bg_start)), end=' ')
    for fg_color in range(fg_start, fg_end + 1):
        print(' ' * (len(test_string) - len(str(fg_color))), fg_color, end=' ')
    print()

    for bg_color in range(bg_start, bg_end + 1):
        print(bg_color, bg(bg_color), end=' ')
        for fg_color in range(fg_start, fg_end + 1):
            print(fg(fg_color), test_string, end=' ')
        print(reset())
