from ..utils import BasicSegment


class Segment(BasicSegment):
    def add_to_powerline(self):
        powerline = self.powerline
        root_indicators = {
            'bash': ' \\$ ',
            'tcsh': ' %# ',
            'zsh': ' %# ',
            'bare': ' $ ',
        }
        bg = powerline.theme.CMD_PASSED_BG
        fg = powerline.theme.CMD_PASSED_FG
        if powerline.args.prev_error != 0:
            fg = powerline.theme.CMD_FAILED_FG
            bg = powerline.theme.CMD_FAILED_BG
        powerline.append(root_indicators[powerline.args.shell], fg, bg, sanitize=False)
