from ..utils import BasicSegment


class Segment(BasicSegment):
    def add_to_powerline(self):
        self.powerline.append("\n",
                              self.powerline.theme.RESET,
                              self.powerline.theme.RESET,
                              separator="")
