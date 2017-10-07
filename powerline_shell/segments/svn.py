import subprocess, os
from ..utils import ThreadedSegment, RepoStats


def get_PATH():
    """Normally gets the PATH from the OS. This function exists to enable
    easily mocking the PATH in tests.
    """
    return os.getenv("PATH")


def svn_subprocess_env():
    return {"PATH": get_PATH()}


def _get_svn_branch():
    p = subprocess.Popen(["svn", "info"],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         env=svn_subprocess_env())
    working_dir_root_path = p.communicate()[0].decode("utf-8").splitlines()[1]
    branch = os.path.basename(working_dir_root_path.split()[-1])
    return branch


def parse_svn_stats(status):
    stats = RepoStats()
    for line in status:
        if line[0] == "?":
            stats.new += 1
        elif line[0] == "C":
            stats.conflicted += 1
        elif line[0] in ["A", "D", "I", "M", "R", "!", "~"]:
            stats.changed += 1
    return stats


def _get_svn_status(output):
    """This function exists to enable mocking the `svn status` output in tests.
    """
    return output[0].decode("utf-8").splitlines()


def build_stats():
    try:
        p = subprocess.Popen(['svn', 'status'],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             env=svn_subprocess_env())
    except OSError:
        # Popen will throw an OSError if svn is not found
        return None
    pdata = p.communicate()
    if p.returncode != 0 or pdata[1][:22] == b'svn: warning: W155007:':
        return None, None
    status = _get_svn_status(pdata)
    stats = parse_svn_stats(status)
    branch = _get_svn_branch()
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
        if self.powerline.segment_conf("vcs", "show_symbol"):
            symbol = RepoStats().symbols["svn"] + " "
        else:
            symbol = ""
        self.powerline.append(" " + symbol + self.branch + " ", fg, bg)
        self.stats.add_to_powerline(self.powerline)
