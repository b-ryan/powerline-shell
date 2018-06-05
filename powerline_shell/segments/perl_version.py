import os
from ..utils import ThreadedSegment


class Segment(ThreadedSegment):
    def run(self):
        if os.getenv('PERLBREW_PERL'): 
            self.version = os.getenv('PERLBREW_PERL')
        else:
            self.version = None

    def add_to_powerline(self):
        self.join()
        if not self.version:
            return
        # FIXME no hard-coded colors
        self.powerline.append(self.version, 15, 4)
