import subprocess
from ..utils import BasicSegment, RepoStats


class Segment(BasicSegment):
    def add_to_powerline(self):
        is_svn = subprocess.Popen(["svn", "status"],
                                  stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        is_svn_output = is_svn.communicate()[1].decode("utf-8").strip()
        if len(is_svn_output) != 0:
            return

        try:
            p1 = subprocess.Popen(["svn", "status"], stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE)
        except OSError:
            return

        stdout = p1.communicate()[0]
        stats = RepoStats()
        for line in stdout.splitlines():
            if line[0] == "?":
                stats.new += 1
            elif line[0] == "C":
                stats.conflicted += 1
            elif line[0] in ["A", "D", "I", "M", "R", "!", "~"]:
                stats.changed += 1

        stats.add_to_powerline(self.powerline)
