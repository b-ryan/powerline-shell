import os
from ..utils import BasicSegment


class Segment(BasicSegment):
    def add_to_powerline(self):
        powerline = self.powerline
        try:
            if os.environ.get('IN_NIX_SHELL'):
                powerline.append(u"\u03BB",
                                 powerline.theme.CWD_FG,
                                 powerline.theme.PATH_BG)
        except OSError:
            return
