import os

def add_nix_shell_segment(powerline):
    if os.environ.get('IN_NIX_SHELL') :
        powerline.append(u"\u03BB", 4, 255)
