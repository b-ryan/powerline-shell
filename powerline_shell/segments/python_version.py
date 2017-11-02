import subprocess
from ..utils import BasicSegment


class Segment(BasicSegment):
    def add_to_powerline(self):
        powerline = self.powerline

        try:

            output = subprocess.check_output(['python', '--version'],
                                             stderr=subprocess.STDOUT)
            version = output.rstrip().split(' ')[1]
            powerline.append(version, 15, 1)
        except OSError:
            return
