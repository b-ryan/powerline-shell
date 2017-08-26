import subprocess
from ..utils import BasicSegment


class Segment(BasicSegment):
    def add_to_powerline(self):
        powerline = self.powerline
        try:
            output = subprocess.check_output(['php', '-r', 'echo PHP_VERSION;'],
                                             stderr=subprocess.STDOUT)
            if '-' in output:
                version = ' %s ' % output.split('-')[0]
            else:
                version = ' %s ' % output
            powerline.append(version, 15, 4)
        except OSError:
            return
