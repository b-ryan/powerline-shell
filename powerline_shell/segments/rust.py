import os
import subprocess
from ..utils import BasicSegment


class Segment(BasicSegment):
    def add_to_powerline(self):
        powerline = self.powerline
        try:
            p1 = subprocess.run(
                ["rustup", "toolchain", "list"], stdout=subprocess.PIPE)
            v = p1.stdout.decode("utf-8")
            for line in v:
                if "(default)" in line:
                    powerline.append(line.split("-"), 15, 1)
        except OSError:
            return
