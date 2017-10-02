import os
import subprocess
from ..utils import RepoStats, ThreadedSegment


def get_PATH():
    """Normally gets the PATH from the OS. This function exists to enable
    easily mocking the PATH in tests.
    """
    return os.getenv("PATH")


def bzr_subprocess_env():
    return {"PATH": get_PATH()}


def _get_bzr_branch():
    p = subprocess.Popen(['bzr', 'nick'],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         env=bzr_subprocess_env())
    branch = p.communicate()[0].decode("utf-8").rstrip('\n')
    return branch


def parse_bzr_stats(status):
    stats = RepoStats()
    statustype = "changed"
    for statusline in status:
        if statusline[:2] == "  ":
            setattr(stats, statustype, getattr(stats, statustype) + 1)
        elif statusline == "added:":
            statustype = "staged"
        elif statusline == "unknown:":
            statustype = "new"
        else:  # removed, missing, renamed, modified or kind changed
            statustype = "changed"
    return stats


def _get_bzr_status(output):
    """This function exists to enable mocking the `bzr status` output in tests.
    """
    return output[0].decode("utf-8").splitlines()


def build_stats():
    try:
        p = subprocess.Popen(['bzr', 'status'],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             env=bzr_subprocess_env())
    except OSError:
        # Popen will throw an OSError if bzr is not found
        return (None, None)
    pdata = p.communicate()
    if p.returncode != 0:
        return (None, None)
    status = _get_bzr_status(pdata)
    stats = parse_bzr_stats(status)
    branch = _get_bzr_branch()
    return stats, branch


class Segment(ThreadedSegment):
    def run(self):
        self.stats, self.branch = build_stats()

    def add_to_powerline(self):
        self.join()
        if not self.stats:
            return
        bg = self.powerline.theme.REPO_CLEAN_BG
        fg = self.powerline.theme.REPO_CLEAN_FG
        if self.stats.dirty:
            bg = self.powerline.theme.REPO_DIRTY_BG
            fg = self.powerline.theme.REPO_DIRTY_FG

        self.powerline.append(" " + self.branch + " ", fg, bg)
        self.stats.add_to_powerline(self.powerline)
