import os
from ..utils import BasicSegment


class Segment(BasicSegment):
    def add_to_powerline(self):
        if os.getenv('ASCIINEMA_REC'):
            powerline = self.powerline
            powerline.append('\33[5m' + u'\u26ab' + '\033[0m',
                             powerline.theme.ASCIINEMA_FG,
                             powerline.theme.ASCIINEMA_BG)
