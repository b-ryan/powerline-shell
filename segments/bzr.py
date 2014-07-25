import os
import subprocess

def get_bzr_status():
    has_modified_files = False
    has_untracked_files = False
    has_missing_files = False
    output = subprocess.Popen(['bzr', 'status'],
            stdout=subprocess.PIPE).communicate()[0]
    if 'unknown:\n' in output:
        has_untracked_files = True
    elif 'removed:\n' in output:
        has_missing_files = True
    elif 'modified:\n' in output:
        has_modified_files = True
    return has_modified_files, has_untracked_files, has_missing_files

def add_bzr_segment():
    branches = os.popen('bzr branches 2> /dev/null').readlines()
    if len(branches) == 0:
        return False
    branch = ''
    for line in branches:
        if line[0] == '*':
            branch = line[2:-1]

    bg = Color.REPO_CLEAN_BG
    fg = Color.REPO_CLEAN_FG
    has_modified_files, has_untracked_files, has_missing_files = get_bzr_status()
    if has_modified_files or has_untracked_files or has_missing_files:
        bg = Color.REPO_DIRTY_BG
        fg = Color.REPO_DIRTY_FG
        extra = ''
        if has_untracked_files:
            extra += '+'
        if has_missing_files:
            extra += '!'
        branch += (' ' + extra if extra != '' else '')
    return powerline.append(' %s ' % branch, fg, bg)

add_bzr_segment()
