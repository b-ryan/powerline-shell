import subprocess
from ..utils import BasicSegment


class Segment(BasicSegment):
    def add_to_powerline(self):
        powerline = self.powerline

        try:
            p1 = subprocess.Popen(["python", "--version"], stdout=subprocess.PIPE)
            p2 = subprocess.Popen(["sed", "s/ (.*//"], stdin=p1.stdout, stdout=subprocess.PIPE)
            version = p2.communicate()[0].decode("utf-8").rstrip()

            powerline.append(version, 15, 1)
        except OSError:
            return
