import os
import subprocess
from ..utils import ThreadedSegment

FANCY_NODE = u'\ue718'


class Segment(ThreadedSegment):
    def run(self):
        try:
            p1 = subprocess.Popen(["node", "--version"], stdout=subprocess.PIPE)
            p2 = subprocess.Popen(['sed', 's/^v//'],
                                  stdin=p1.stdout,
                                  stdout=subprocess.PIPE)
            self.version = p2.communicate()[0].decode("utf-8").rstrip()
        except OSError:
            self.version = None

    def add_to_powerline(self):
        # Do not render node version segment unless .ruby-version file exists
        if not os.path.isfile('.node-version'):
            return

        self.join()
        if not self.version:
            return

        if self.powerline.segment_conf('node_version', 'mode') == 'fancy':
            self.version = u'{} {}'.format(FANCY_NODE, self.version)

        self.powerline.append(' %s ' % self.version, self.powerline.theme.VIRTUAL_ENV_FG, self.powerline.theme.VIRTUAL_ENV_BG)
