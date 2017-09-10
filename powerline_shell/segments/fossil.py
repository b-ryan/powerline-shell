import os
import subprocess
from ..utils import ThreadedSegment


def get_fossil_branch():
    try:
        subprocess.Popen(['fossil'], stdout=subprocess.PIPE).communicate()
    except OSError:
        return None
    return ''.join([
        i.replace('*','').strip()
        for i in os.popen("fossil branch 2> /dev/null").read().strip().split("\n")
        if i.startswith('*')
    ])


def get_fossil_status():
    has_modified_files = False
    has_untracked_files = False
    has_missing_files = False
    output = os.popen('fossil changes 2>/dev/null').read().strip()
    has_untracked_files = bool(
        os.popen("fossil extras 2>/dev/null").read().strip()
    )
    has_missing_files = 'MISSING' in output
    has_modified_files = 'EDITED' in output
    return has_modified_files, has_untracked_files, has_missing_files


class Segment(ThreadedSegment):
    def run(self):
        self.branch = get_fossil_branch()
        self.status = get_fossil_status() if self.branch else None

    def add_to_powerline(self):
        self.join()
        powerline = self.powerline
        if not self.branch or not self.status:
            return
        has_modified, has_untracked, has_missing = self.status
        bg = powerline.theme.REPO_CLEAN_BG
        fg = powerline.theme.REPO_CLEAN_FG
        if has_modified or has_untracked or has_missing:
            bg = powerline.theme.REPO_DIRTY_BG
            fg = powerline.theme.REPO_DIRTY_FG
            extra = ''
            if has_untracked:
                extra += '+'
            if has_missing:
                extra += '!'
            self.branch += (' ' + extra if extra != '' else '')
        powerline.append(' %s ' % self.branch, fg, bg)
