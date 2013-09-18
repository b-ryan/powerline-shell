import os

def add_read_only_segment():
    cwd = powerline.cwd or os.getenv('PWD')

    READONLY_BG = getattr(Color, 'READONLY_BG', 124)
    READONLY_FG = getattr(Color, 'READONLY_FG', 254)

    if not os.access(cwd, os.W_OK):
        powerline.append(' %s ' % powerline.lock, READONLY_FG, READONLY_BG)

add_read_only_segment()