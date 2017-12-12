import subprocess
from ..utils import ThreadedSegment, RepoStats


class Segment(ThreadedSegment):
    def __init__(self, powerline):
        super(Segment, self).__init__(powerline)
        self.stats = None
        self.revision = ""

    def run(self):
        try:
            svn_status = subprocess.Popen(["svn", "status"],
                                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            svn_info = subprocess.Popen(["svn", "info"],
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            svn_stdout, svn_stderr = svn_status.communicate()
            svn_info, _ = svn_info.communicate()
        except OSError:
            return

        if len(svn_stderr.decode("utf-8").strip()) != 0:
            return

        self.stats = RepoStats()
        for line in svn_stdout.splitlines():
            line = line.decode("utf-8").strip()
            if line[0] == "?":
                self.stats.new += 1
            elif line[0] == "C":
                self.stats.conflicted += 1
            elif line[0] in ["A", "D", "I", "M", "R", "!", "~"]:
                self.stats.changed += 1

        for line in svn_info.splitlines():
            line = line.decode("utf-8").strip()
            if "Revision: " in line:
                self.revision = line.split(" ", maxsplit=1)[1]

    def add_to_powerline(self):
        self.join()
        if not self.stats:
            return
        bg = self.powerline.theme.REPO_CLEAN_BG
        fg = self.powerline.theme.REPO_CLEAN_FG
        if self.stats.dirty:
            bg = self.powerline.theme.REPO_DIRTY_BG
            fg = self.powerline.theme.REPO_DIRTY_FG

        self.powerline.append(" rev " + self.revision + " ", fg, bg)
        self.stats.add_to_powerline(self.powerline)
