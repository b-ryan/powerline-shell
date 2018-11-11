import sys
import os
import threading

py3 = sys.version_info[0] == 3

if py3:
    def unicode_(x):
        return str(x)
    def decode(x):
        return x.decode("utf-8")
else:
    unicode_ = unicode
    decode = unicode


class RepoStats(object):
    symbols = {
        'detached': u'\u2693',
        'ahead': u'\u2B06',
        'behind': u'\u2B07',
        'staged': u'\u2714',
        'changed': u'\u270E',
        'new': u'?',
        'conflicted': u'\u273C',
        'stash': u'\u2398',
        'git': u'\uE0A0',
        'hg': u'\u263F',
        'bzr': u'\u2B61\u20DF',
        'fossil': u'\u2332',
        'svn': u'\u2446'
    }

    def __init__(self, ahead=0, behind=0, new=0, changed=0, staged=0, conflicted=0):
        self.ahead = ahead
        self.behind = behind
        self.new = new
        self.changed = changed
        self.staged = staged
        self.conflicted = conflicted

    def __eq__(self, other):
        return (
            self.ahead == other.ahead and
            self.behind == other.behind and
            self.new == other.new and
            self.changed == other.changed and
            self.staged == other.staged and
            self.conflicted == other.conflicted
        )

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
        return unicode_(self[_key]) if int(self[_key]) > 1 else u''

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
    def __init__(self, powerline, segment_def):
        self.powerline = powerline
        self.segment_def = segment_def  # type: dict

    def start(self):
        pass


class ThreadedSegment(threading.Thread):
    def __init__(self, powerline, segment_def):
        super(ThreadedSegment, self).__init__()
        self.powerline = powerline
        self.segment_def = segment_def  # type: dict


def import_file(module_name, path):
    # An implementation of https://stackoverflow.com/a/67692/683436
    if py3 and sys.version_info[1] >= 5:
        import importlib.util
        spec = importlib.util.spec_from_file_location(module_name, path)
        if not spec:
            raise ImportError()
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    elif py3:
        from importlib.machinery import SourceFileLoader
        return SourceFileLoader(module_name, path).load_module()
    else:
        import imp
        return imp.load_source(module_name, path)


def get_PATH():
    """Normally gets the PATH from the OS. This function exists to enable
    easily mocking the PATH in tests.
    """
    return os.getenv("PATH")


def get_subprocess_env(**envs):
    defaults = {
        # https://github.com/milkbikis/powerline-shell/pull/153
        "PATH": get_PATH(),
    }
    defaults.update(envs)
    env = dict(os.environ)
    env.update(defaults)
    return env


def get_git_subprocess_env():
    # LANG is specified to ensure git always uses a language we are expecting.
    # Otherwise we may be unable to parse the output.
    return get_subprocess_env(LANG="C")

