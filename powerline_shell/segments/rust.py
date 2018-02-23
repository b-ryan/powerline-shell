import os
import subprocess
from ..utils import BasicSegment


class Segment(BasicSegment):
    def add_to_powerline(self):
        powerline = self.powerline
        try:
            c1 = subprocess.Popen(["ls"], stdout=subprocess.PIPE)
            c2 = subprocess.Popen(["grep", "'\(Cargo.toml\)\|\(.*.rs\)'"],
                                  stdin=c1.stdout, stdout=subprocess.PIPE)
            has_cargo = c2.communicate()[0].decode("utf-8")
            if len(has_cargo) > 0:
                p1 = subprocess.Popen(
                    ["rustc", "--version"], stdout=subprocess.PIPE)
                line = p1.communicate()[0].decode("utf-8")
                powerline.append(line.split(" ")[1], 232, 130)
        except OSError:
            return
