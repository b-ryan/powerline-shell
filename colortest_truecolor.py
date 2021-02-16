#!/usr/bin/env python2
import sys

ESCAPE = chr(27)

def fg(color):
    return ESCAPE + '[38;2;%d;%d;%dm' % color

def bg(color):
    return ESCAPE + '[48;2;%d;%d;%dm' % color

def reset():
    return ESCAPE + '[48;0m'

if __name__ == "__main__":
    if len(sys.argv) < 8:
        print 'Usage: colortest_truecolor.py fg_red fg_green fg_blue bg_red bg_green bg_blue test_string'
        sys.exit(1)
    
    fg_red, fg_green, fg_blue, bg_red, bg_green, bg_blue = map(int, sys.argv[1:-1])
    test_string = sys.argv[-1]

    print bg((bg_red, bg_green, bg_blue)), fg((fg_red, fg_green, fg_blue)), test_string, reset()
