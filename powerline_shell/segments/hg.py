import os
import subprocess
from ..utils import ThreadedSegment


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


class Segment(ThreadedSegment):
    def run(self):
        self.branch = os.popen('hg branch 2> /dev/null').read().rstrip()
        self.status = get_hg_status() if self.branch else None

    def add_to_powerline(self):
        self.join()
        if not self.branch or not self.status:
            return
        bg = self.powerline.theme.REPO_CLEAN_BG
        fg = self.powerline.theme.REPO_CLEAN_FG
        has_modified, has_untracked, has_missing = self.status
        if has_modified or has_untracked or has_missing:
            bg = self.powerline.theme.REPO_DIRTY_BG
            fg = self.powerline.theme.REPO_DIRTY_FG
            extra = ''
            if has_untracked:
                extra += '+'
            if has_missing:
                extra += '!'
            branch += (' ' + extra if extra != '' else '')
        return powerline.append(' %s ' % branch, fg, bg)
