import subprocess
from ..utils import RepoStats, ThreadedSegment, get_subprocess_env


def _get_hg_branch():
    p = subprocess.Popen(["hg", "branch"],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         env=get_subprocess_env())
    branch = p.communicate()[0].decode("utf-8").rstrip('\n')
    return branch


def parse_hg_stats(status):
    stats = RepoStats()
    for statusline in status:
        if statusline[0] == "A":
            stats.staged += 1
        elif statusline[0] == "?":
            stats.new += 1
        else:  # [M]odified, [R]emoved, (!)missing
            stats.changed += 1
    return stats


def _get_hg_status(output):
    """This function exists to enable mocking the `hg status` output in tests.
    """
    return output[0].decode("utf-8").splitlines()


def build_stats():
    try:
        p = subprocess.Popen(["hg", "status"],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE,
                             env=get_subprocess_env())
    except OSError:
        # Will be thrown if hg cannot be found
        return None, None
    pdata = p.communicate()
    if p.returncode != 0:
        return None, None
    status = _get_hg_status(pdata)
    stats = parse_hg_stats(status)
    branch = _get_hg_branch()
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
            symbol = RepoStats().symbols["hg"] + " "
        else:
            symbol = ""
        self.powerline.append(" " + symbol + self.branch + " ", fg, bg)
        self.stats.add_to_powerline(self.powerline)
