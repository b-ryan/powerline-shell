import os
from ..utils import BasicSegment
import subprocess


class Segment(BasicSegment):
    def add_to_powerline(self):
        if subprocess.Popen(['sudo', '-n', 'echo', '-n', '1'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE).communicate()[0] == b'1':
            self.powerline.append(" # ", self.powerline.theme.SUDO_FG, self.powerline.theme.SUDO_BG)
