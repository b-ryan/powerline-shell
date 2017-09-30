import os
from ..utils import BasicSegment


class Segment(BasicSegment):
    def add_to_powerline(self):
        powerline = self.powerline
        cwd = powerline.cwd or os.getenv('PWD')
        if not os.access(cwd, os.W_OK):
            powerline.append(' %s ' % powerline.lock,
                             powerline.theme.READONLY_FG,
                             powerline.theme.READONLY_BG)
