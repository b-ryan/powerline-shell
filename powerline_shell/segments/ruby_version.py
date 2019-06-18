import os
import subprocess
from ..utils import BasicSegment

FANCY_RUBY = u'\ue791'
FANCY_NODE = u'\ue718'

SYSTEM_NODE_VERSION = '7.10.0'
SYSTEM_RUBY_VERSION = 'ruby 2.5.3p105'


def _get_node_version():
    try:
        p1 = subprocess.Popen(['node', '-v'], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(['sed', 's/^v//'],
                              stdin=p1.stdout,
                              stdout=subprocess.PIPE)
        return p2.communicate()[0].decode('utf-8').rstrip()
    except OSError:
        raise


def _get_ruby_version():
    try:
        p1 = subprocess.Popen(['ruby', '-v'], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(['sed', 's/ (.*//'],
                              stdin=p1.stdout,
                              stdout=subprocess.PIPE)
        return p2.communicate()[0].decode('utf-8').rstrip()
    except OSError:
        raise


class Segment(BasicSegment):
    def add_to_powerline(self):
        powerline = self.powerline

        try:
            ruby_version = _get_ruby_version()
            node_version = _get_node_version()
        except OSError:
            return

        if ruby_version == SYSTEM_RUBY_VERSION:
            ruby_version = '%s ' % FANCY_RUBY
        elif powerline.segment_conf('ruby_version', 'mode') == 'fancy':
            ruby_version = ruby_version.replace('ruby', FANCY_RUBY)
        else:
            pass

        gem_set = os.environ.get('GEM_HOME', '').split('@')[1:]
        if gem_set:
            ruby_version += "@{}".format(gem_set.pop())
        if ruby_version:
            powerline.append(' %s ' % ruby_version, powerline.theme.RUBY_FG, powerline.theme.RUBY_BG)

        if node_version != SYSTEM_NODE_VERSION:
            node_string = u'{} {}'.format(FANCY_NODE, node_version)
            powerline.append(' %s ' % node_string, powerline.theme.VIRTUAL_ENV_FG, powerline.theme.VIRTUAL_ENV_BG)
