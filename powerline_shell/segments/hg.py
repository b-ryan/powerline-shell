import os
import subprocess
from ..utils import BasicSegment


def get_hg_status():
    has_modified_files = False
    has_untracked_files = False
    has_missing_files = False

    p = subprocess.Popen(['hg', 'status'], stdout=subprocess.PIPE)
    output = p.communicate()[0].decode("utf-8")

    for line in output.split('\n'):
        if line == '':
            continue
        elif line[0] == '?':
            has_untracked_files = True
        elif line[0] == '!':
            has_missing_files = True
        else:
            has_modified_files = True
    return has_modified_files, has_untracked_files, has_missing_files


class Segment(BasicSegment):
    def add_to_powerline(self):
        powerline = self.powerline
        branch = os.popen('hg branch 2> /dev/null').read().rstrip()
        if len(branch) == 0:
            return False
        bg = powerline.theme.REPO_CLEAN_BG
        fg = powerline.theme.REPO_CLEAN_FG
        has_modified_files, has_untracked_files, has_missing_files = get_hg_status()
        if has_modified_files or has_untracked_files or has_missing_files:
            bg = powerline.theme.REPO_DIRTY_BG
            fg = powerline.theme.REPO_DIRTY_FG
            extra = ''
            if has_untracked_files:
                extra += '+'
            if has_missing_files:
                extra += '!'
            branch += (' ' + extra if extra != '' else '')
        return powerline.append(' %s ' % branch, fg, bg)
