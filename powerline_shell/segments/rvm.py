import os
from ..utils import BasicSegment


class Segment(BasicSegment):
    def add_to_powerline(self):
        powerline = self.powerline
        try:
            ruby_version = os.environ.get('RUBY_VERSION')
            gem_home = os.environ.get('GEM_HOME')
            gem_set = None

            if gem_home:
                gem_home_parts = gem_home.split('@', 2)
                if len(gem_home_parts) > 1:
                    gem_set = gem_home_parts[1]

            # print only when using a defined ruby version
            # empty when using system ruby
            if ruby_version:
                text = ruby_version
                if gem_set:
                    text += '@' + gem_set

                powerline.append(' %s ' % text,
                                 powerline.theme.VIRTUAL_ENV_FG,
                                 powerline.theme.VIRTUAL_ENV_BG)
        except OSError:
            return
