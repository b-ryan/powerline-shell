from ..utils import BasicSegment
import time


class Segment(BasicSegment):
    def add_to_powerline(self):
        powerline = self.powerline
        if powerline.args.shell == 'bash':
            time = ' \\t '
        elif powerline.args.shell == 'zsh':
            time = ' %* '
        else:
            time = ' %s ' % time.strftime('%H:%M:%S')
        powerline.append(time,
                         powerline.theme.HOSTNAME_FG,
                         powerline.theme.HOSTNAME_BG)
