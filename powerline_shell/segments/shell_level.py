import os
from ..utils import BasicSegment


class Segment(BasicSegment):
    def add_to_powerline(self):
        lvl = os.getenv('SHLVL')
        if not lvl or (lvl.isdigit() and int(lvl)==1):
            return
        bg = self.powerline.theme.SHELL_LEVEL_BG
        fg = self.powerline.theme.SHELL_LEVEL_FG
        self.powerline.append("⏫ " + lvl + " ", fg, bg)
