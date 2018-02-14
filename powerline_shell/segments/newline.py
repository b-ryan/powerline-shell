from ..utils import BasicSegment, warn


class Segment(BasicSegment):
    def add_to_powerline(self):
        if self.powerline.args.shell == "tcsh":
            warn("newline segment not supported for tcsh (yet?)")
            return
        self.powerline.append("\n",
                              self.powerline.theme.RESET,
                              self.powerline.theme.RESET,
                              separator="")
