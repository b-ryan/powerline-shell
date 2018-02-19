import os
from ..utils import BasicSegment


class Segment(BasicSegment):
    def add_to_powerline(self):
        self.powerline.append(
            " %s " % os.getenv(self.segment_def["var"]),
            self.segment_def.get("fg_color", self.powerline.theme.STDOUT_DEFAULT_FG),
            self.segment_def.get("bg_color", self.powerline.theme.STDOUT_DEFAULT_BG))
