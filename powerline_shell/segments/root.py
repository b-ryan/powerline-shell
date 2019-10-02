from ..utils import BasicSegment


class Segment(BasicSegment):
    def add_to_powerline(self):
        powerline = self.powerline
        indicator = self._get_indicator(powerline.args.shell, powerline)
        bg = powerline.theme.CMD_PASSED_BG
        fg = powerline.theme.CMD_PASSED_FG
        if powerline.args.prev_error != 0:
            fg = powerline.theme.CMD_FAILED_FG
            bg = powerline.theme.CMD_FAILED_BG
        powerline.append(indicator, fg, bg, sanitize=False)

    def _get_indicator(self, shell, powerline):
        custom_indicator = powerline.segment_conf("root", "indicator", None)
        root_indicators = {
            'bash': ' \\$ ',
            'tcsh': ' %# ',
            'zsh': ' %# ',
            'bare': ' $ ',
        }
        return custom_indicator or root_indicators[shell]
