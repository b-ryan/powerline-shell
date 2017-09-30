import os
from ..utils import BasicSegment


class Segment(BasicSegment):
    def add_to_powerline(self):
        if os.getenv('SSH_CLIENT'):
            powerline = self.powerline
            powerline.append(' %s ' % powerline.network,
                             powerline.theme.SSH_FG,
                             powerline.theme.SSH_BG)
