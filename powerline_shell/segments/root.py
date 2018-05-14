from ..utils import BasicSegment
from os import geteuid


class Segment(BasicSegment):
    def add_to_powerline(self):
        powerline = self.powerline
        root_indicators = {
            'bash': ' \\$ ',
            'tcsh': ' %# ',
            'zsh': ' %# ',
            'bare': ' $ ',
        }
        if powerline.segment_conf("root", "indicator") and geteuid():
            indicator = powerline.segment_conf("root", "indicator")
        else:
            indicator = root_indicators[powerline.args.shell]
        bg = powerline.theme.CMD_PASSED_BG
        fg = powerline.theme.CMD_PASSED_FG
        if powerline.args.prev_error != 0:
            fg = powerline.theme.CMD_FAILED_FG
            bg = powerline.theme.CMD_FAILED_BG
        powerline.append(indicator, fg, bg, sanitize=False)
