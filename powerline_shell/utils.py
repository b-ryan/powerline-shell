import sys
import threading

py3 = sys.version_info[0] == 3

if py3:
    def unicode(x):
        return x


class RepoStats(object):
    symbols = {
        'detached': u'\u2693',
        'ahead': u'\u2B06',
        'behind': u'\u2B07',
        'staged': u'\u2714',
        'changed': u'\u270E',
        'new': u'\u2753',
        'conflicted': u'\u273C'
    }

    def __init__(self):
        self.ahead = 0
        self.behind = 0
        self.new = 0
        self.changed = 0
        self.staged = 0
        self.conflicted = 0

    @property
    def dirty(self):
        qualifiers = [
            self.new,
            self.changed,
            self.staged,
            self.conflicted,
        ]
        return sum(qualifiers) > 0

    def __getitem__(self, _key):
        return getattr(self, _key)

    def n_or_empty(self, _key):
        """Given a string name of one of the properties of this class, returns
        the value of the property as a string when the value is greater than
        1. When it is not greater than one, returns an empty string.

        As an example, if you want to show an icon for new files, but you only
        want a number to appear next to the icon when there are more than one
        new file, you can do:

            segment = repo_stats.n_or_empty("new") + icon_string
        """
        return unicode(self[_key]) if int(self[_key]) > 1 else u''

    def add_to_powerline(self, powerline):
        def add(_key, fg, bg):
            if self[_key]:
                s = u" {}{} ".format(self.n_or_empty(_key), self.symbols[_key])
                powerline.append(s, fg, bg)
        color = powerline.theme
        add('ahead', color.GIT_AHEAD_FG, color.GIT_AHEAD_BG)
        add('behind', color.GIT_BEHIND_FG, color.GIT_BEHIND_BG)
        add('staged', color.GIT_STAGED_FG, color.GIT_STAGED_BG)
        add('changed', color.GIT_NOTSTAGED_FG, color.GIT_NOTSTAGED_BG)
        add('new', color.GIT_UNTRACKED_FG, color.GIT_UNTRACKED_BG)
        add('conflicted', color.GIT_CONFLICTED_FG, color.GIT_CONFLICTED_BG)


def warn(msg):
    print('[powerline-bash] ', msg)


class BasicSegment(object):
    def __init__(self, powerline):
        self.powerline = powerline

    def start(self):
        pass


class ThreadedSegment(threading.Thread):
    def __init__(self, powerline):
        super(ThreadedSegment, self).__init__()
        self.powerline = powerline
