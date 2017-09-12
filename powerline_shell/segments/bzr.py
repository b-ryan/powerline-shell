import os
import subprocess
from ..utils import ThreadedSegment


def get_PATH():
    """Normally gets the PATH from the OS. This function exists to enable
    easily mocking the PATH in tests.
    """
    return os.getenv("PATH")


def _subprocess_env():
    return {"PATH": get_PATH()}


def get_bzr_status():
    has_modified_files = False
    has_untracked_files = False
    has_missing_files = False
    p = subprocess.Popen(['bzr', 'status'],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         env=_subprocess_env())
    output = p.communicate()[0].decode("utf-8")
    if 'unknown:\n' in output:
        has_untracked_files = True
    elif 'removed:\n' in output:
        has_missing_files = True
    elif 'modified:\n' in output:
        has_modified_files = True
    return has_modified_files, has_untracked_files, has_missing_files


def build_stats():
    try:
        p = subprocess.Popen(["bzr", "nick"],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             env=_subprocess_env())
    except OSError:
        # Will be thrown if bzr cannot be found
        return None, None

    pdata = p.communicate()
    if p.returncode != 0:
        return None, None

    branch = pdata[0].decode("utf-8").strip()
    return branch, get_bzr_status()


class Segment(ThreadedSegment):
    def run(self):
        self.branch, self.status = build_stats()

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
            extra = ""
            if has_untracked:
                extra += "+"
            if has_missing:
                extra += "!"
            self.branch += " " + extra
        return self.powerline.append(" %s " % self.branch, fg, bg)

