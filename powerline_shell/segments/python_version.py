import subprocess
from ..utils import ThreadedSegment, decode


class Segment(ThreadedSegment):
    def run(self):
        try:
            output = decode(
                subprocess.check_output(["python", "--version"],
                                        stderr=subprocess.STDOUT))
            self.version = output.rstrip().lower()
        except OSError:
            self.version = None

    def add_to_powerline(self):
        self.join()
        if not self.version:
            return
        # FIXME no hard-coded colors
        self.powerline.append(self.version, 15, 4)
