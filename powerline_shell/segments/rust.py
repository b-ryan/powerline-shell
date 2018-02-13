import os
import subprocess
from ..utils import BasicSegment


class Segment(BasicSegment):
    def add_to_powerline(self):
        powerline = self.powerline
        try:
            c1 = subprocess.Popen(["ls"], stdout=subprocess.PIPE)
            c2 = subprocess.Popen(["grep", "Cargo.toml"],
                                  stdin=c1.stdout, stdout=subprocess.PIPE)
            has_cargo = c2.communicate()[0].decode("utf-8")
            if len(has_cargo) > 0:
                p1 = subprocess.Popen(
                    ["rustup", "toolchain", "list"], stdout=subprocess.PIPE)
                v = p1.communicate()[0].decode("utf-8")
                for line in v.split("\n"):
                    if u"(default)" in line:
                        powerline.append(line.split("-")[0], 15, 1)
                        return
        except OSError:
            return
