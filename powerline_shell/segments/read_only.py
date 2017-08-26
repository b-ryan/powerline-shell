import os

def add_read_only_segment(powerline):
    cwd = powerline.cwd or os.getenv('PWD')

    if not os.access(cwd, os.W_OK):
        powerline.append(' %s ' % powerline.lock, powerline.theme.READONLY_FG, powerline.theme.READONLY_BG)
