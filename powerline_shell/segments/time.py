from __future__ import absolute_import
from ..utils import BasicSegment
import time


class Segment(BasicSegment):
    def add_to_powerline(self):
        powerline = self.powerline
        format = powerline.segment_conf('time', 'format')
        if format:
            time_ = ' %s ' % time.strftime(format)
        elif powerline.args.shell == 'bash':
            time_ = ' \\t '
        elif powerline.args.shell == 'zsh':
            time_ = ' %* '
        else:
            time_ = ' %s ' % time.strftime('%H:%M:%S')
        powerline.append(time_,
                         powerline.theme.TIME_FG,
                         powerline.theme.TIME_BG)
