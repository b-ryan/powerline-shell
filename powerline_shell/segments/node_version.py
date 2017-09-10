import subprocess
from ..utils import ThreadedSegment


class Segment(ThreadedSegment):
    def run(self):
        try:
            p1 = subprocess.Popen(["node", "--version"], stdout=subprocess.PIPE)
            self.version = p1.communicate()[0].decode("utf-8").rstrip()
        except OSError:
            self.version = None

    def add_to_powerline(self):
        self.join()
        if not self.version:
            return
        # FIXME no hard-coded colors
        self.powerline.append("node " + self.version, 15, 18)
