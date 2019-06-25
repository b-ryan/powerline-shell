import os
import subprocess
from ..utils import ThreadedSegment

FANCY_RUBY = u'\ue23e'


class Segment(ThreadedSegment):
    def run(self):
        try:
            p1 = subprocess.Popen(['ruby', '-v'], stdout=subprocess.PIPE)
            p2 = subprocess.Popen(['sed', 's/ (.*//'],
                                  stdin=p1.stdout,
                                  stdout=subprocess.PIPE)
            self.version = p2.communicate()[0].decode('utf-8').rstrip()
        except OSError:
            self.version = None

    def add_to_powerline(self):
        # Do not render ruby version segment unless .ruby-version file exists
        if not os.path.isfile('.ruby-version'):
            return

        self.join()
        if not self.version:
            return

        if self.powerline.segment_conf('ruby_version', 'mode') == 'fancy':
            self.version = self.version.replace('ruby', FANCY_RUBY)

        gem_set = os.environ.get('GEM_HOME', '').split('@')[1:]
        if gem_set:
            self.version += "@{}".format(gem_set.pop())

        if self.version:
            self.powerline.append(' %s ' % self.version, self.powerline.theme.RUBY_FG, self.powerline.theme.RUBY_BG)
