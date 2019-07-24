import os
from ..utils import BasicSegment


class Segment(BasicSegment):
    def add_to_powerline(self):
        env = os.getenv(self.segment_def["var"])
        if env is None:
            env = self.segment_def["default"]
        if env is not None:
            self.powerline.append(
                " %s " % env,
                self.segment_def.get("fg_color", self.powerline.theme.PATH_FG),
                self.segment_def.get("bg_color", self.powerline.theme.PATH_BG))
