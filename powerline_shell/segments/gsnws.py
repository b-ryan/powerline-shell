import re
import os
from ..utils import BasicSegment

def get_gsnws_name():
    pat_match = re.match('^\w{7}__ndpgsn_5_0_(?:wb__ndpgsn_5_0_(\w+)|(\w+))$', os.getenv('GSN_WS_NAME'))
    if pat_match.group(1):
        return pat_match.group(1)
    if pat_match.group(2):
        return pat_match.group(2)
    return gsnws


class Segment(BasicSegment):
    def add_to_powerline(self):
        if not os.getenv('GSN_WS_NAME'):
            pass
        else: 
            gsnws = get_gsnws_name()
            bg = self.powerline.theme.GSNWS_BG
            fg = self.powerline.theme.GSNWS_FG

            self.powerline.append(" " + gsnws + " ", fg, bg)

