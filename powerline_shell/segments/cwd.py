import os
import sys
from ..utils import warn, py3, BasicSegment

ELLIPSIS = u'\u2026'


def replace_home_dir(cwd):
    home = os.path.realpath(os.getenv('HOME'))
    if cwd.startswith(home):
        return '~' + cwd[len(home):]
    return cwd


def split_path_into_names(cwd):
    names = cwd.split(os.sep)

    if names[0] == '':
        names = names[1:]

    if not names[0]:
        return ['/']

    return names


def requires_special_home_display(powerline, name):
    """Returns true if the given directory name matches the home indicator and
    the chosen theme should use a special home indicator display."""
    return (name == '~' and powerline.theme.HOME_SPECIAL_DISPLAY)


def maybe_shorten_name(powerline, name):
    """If the user has asked for each directory name to be shortened, will
    return the name up to their specified length. Otherwise returns the full
    name."""
    
    max_size = powerline.segment_conf("cwd", "max_dir_size")
    
    if max_size:
        return name[:max_size]
    return name


def get_fg_bg(powerline, name, is_last_dir):
    """Returns the foreground and background color to use for the given name.
    """
    if requires_special_home_display(powerline, name):
        return (powerline.theme.HOME_FG, powerline.theme.HOME_BG,)

    if is_last_dir:
        return (powerline.theme.CWD_FG, powerline.theme.PATH_BG,)
    else:
        return (powerline.theme.PATH_FG, powerline.theme.PATH_BG,)

def conf_last_max_dir_size(powerline, default):
    '''
    last_max_dir_size can be all, full, none, empty, one, or a positive number
    all,full returns -1 ; none,empty returns 0 ; one returns 1
    default accepts a default value which is used if no valid value is configured
    Returns -1 for full size or length of the last max dir size from the settings
    '''
    last_max_size = default
    raw = powerline.segment_conf("cwd", "last_max_dir_size", default)
    if isinstance(raw, str):
        raw = raw.lower()
    if raw is None or raw=="":
        pass
    elif raw=="all" or raw=="full":
        last_max_size = -1
    elif raw=="none" or raw=="empty":
        last_max_size = 0
    elif raw=="one":
        last_max_size = 1
    else:
        try:
            last_max_size = int(raw)
        except ValueError:
            warn("'%s' is not a valid number for cwd.last_max_dir_size, using %s." % (raw, last_max_size))
    return last_max_size

def add_cwd_segment(powerline):
    cwd = powerline.cwd or os.getenv('PWD')
    if not py3:
        cwd = cwd.decode("utf-8")
    cwd = replace_home_dir(cwd)

    if powerline.segment_conf("cwd", "mode") == 'plain':
        powerline.append(' %s ' % (cwd,), powerline.theme.CWD_FG, powerline.theme.PATH_BG)
        return

    names = split_path_into_names(cwd)

    max_size = powerline.segment_conf("cwd", "max_dir_size")
    #last_max_size = powerline.segment_conf("cwd", "last_max_dir_size", max_size)
    last_max_size = conf_last_max_dir_size(powerline, max_size)
    max_depth = powerline.segment_conf("cwd", "max_depth", 5)
    if max_depth <= 0:
        warn("Ignoring cwd.max_depth option since it's not greater than 0")
    elif len(names) > max_depth:
        # https://github.com/milkbikis/powerline-shell/issues/148
        # n_before is the number is the number of directories to put before the
        # ellipsis. So if you are at ~/a/b/c/d/e and max depth is 4, it will
        # show `~ a ... d e`.
        #
        # max_depth must be greater than n_before or else you end up repeating
        # parts of the path with the way the splicing is written below.
        n_before = 2 if max_depth > 2 else max_depth - 1
        names = names[:n_before] + [ELLIPSIS] + names[n_before - max_depth:]

    if powerline.segment_conf("cwd", "mode") == "dironly":
        # The user has indicated they only want the current directory to be
        # displayed, so chop everything else off
        names = names[-1:]

    for i, name in enumerate(names):
        is_last_dir = (i == len(names) - 1)
        fg, bg = get_fg_bg(powerline, name, is_last_dir)

        separator = powerline.separator_thin
        separator_fg = powerline.theme.SEPARATOR_FG
        if requires_special_home_display(powerline, name) or is_last_dir:
            separator = None
            separator_fg = None
        
        formated_name = ""
        
        # if last_max_size is below 0 then assume full name
        if is_last_dir:
            if last_max_size < 0:
                formated_name = name
            elif last_max_size >= 0: #yes, 0 is valid
                formated_name = name[:last_max_size]
        else:
            formated_name = maybe_shorten_name(powerline, name)
        powerline.append(' %s '%formated_name, fg, bg, separator, separator_fg)

class Segment(BasicSegment):
    def add_to_powerline(self):
        add_cwd_segment(self.powerline)
