import os
import subprocess
from ..utils import BasicSegment

FANCY_RUBY = u'\ue791'

def _get_ruby_version():
    try:
        p1 = subprocess.Popen(['ruby', '-v'], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(['sed', "s/ (.*//"], stdin=p1.stdout, stdout=subprocess.PIPE)
        return p2.communicate()[0].decode('utf-8').rstrip()
    except OSError:
        raise

class Segment(BasicSegment):
    def add_to_powerline(self):
        powerline = self.powerline

        try:
            ruby_and_gemset = _get_ruby_version()
        except OSError:
            return

        if powerline.segment_conf("ruby_version", "mode") == "fancy":
            ruby_and_gemset = ruby_and_gemset.replace('ruby', FANCY_RUBY)

        gem_set = os.environ.get('GEM_HOME', '').split('@')[1:]

        if gem_set:
            ruby_and_gemset += "@{}".format(gem_set.pop())

        powerline.append(' %s ' % ruby_and_gemset, powerline.theme.RUBY_FG, powerline.theme.RUBY_BG)
