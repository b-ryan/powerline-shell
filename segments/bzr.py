import os
import subprocess

def get_bzr_status():
    has_modified_files = False
    has_untracked_files = False
    output = subprocess.Popen(['bzr', 'status', '--short'], stdout=subprocess.PIPE).communicate()[0]
    for line in output.split('\n'):
        if line == '':
            continue
        elif line[0] == '?':
            has_untracked_files = True
        else:
            has_modified_files = True
    return has_modified_files, has_untracked_files

def add_bzr_segment():
    bg = Color.REPO_CLEAN_BG
    fg = Color.REPO_CLEAN_FG
    has_modified_files, has_untracked_files = get_bzr_status()
    if has_modified_files or has_untracked_files:
        bg = Color.REPO_DIRTY_BG
        fg = Color.REPO_DIRTY_FG
        extra = ''
        if has_untracked_files:
            extra += '+'
        branch += (' ' + extra if extra != '' else '')
    return powerline.append(' %s ' % branch, fg, bg)

add_bzr_segment()
