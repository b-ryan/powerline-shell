import os


def replace_home_dir(cwd):
    home = os.getenv('HOME')
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


def requires_special_home_display(name):
    """Returns true if the given directory name matches the home indicator and
    the chosen theme should use a special home indicator display."""
    return (name == '~' and Color.HOME_SPECIAL_DISPLAY)


def maybe_shorten_name(name):
    """If the user has asked for each directory name to be shortened, will
    return the name up to their specified length. Otherwise returns the full
    name."""
    if powerline.args.cwd_max_dir_size:
        return name[:powerline.args.cwd_max_dir_size]
    return name


def get_fg_bg(name):
    """Returns the foreground and background color to use for the given name.
    """
    if requires_special_home_display(name):
        return (Color.HOME_FG, Color.HOME_BG,)
    return (Color.PATH_FG, Color.PATH_BG,)


def add_cwd_segment():
    cwd = (powerline.cwd or os.getenv('PWD')).decode('utf-8')
    cwd = replace_home_dir(cwd)
    names = split_path_into_names(cwd)

    max_depth = powerline.args.cwd_max_depth
    if len(names) > max_depth:
        names = names[:2] + [u'\u2026'] + names[2 - max_depth:]

    if powerline.args.cwd_mode == 'plain':
        powerline.append(' %s ' % (cwd,), Color.CWD_FG, Color.PATH_BG)
    else:
        if (powerline.args.cwd_mode == 'dironly' or powerline.args.cwd_only):
            # The user has indicated they only want the current directory to be
            # displayed, so chop everything else off
            names = names[-1:]

        for i, name in enumerate(names):
            fg, bg = get_fg_bg(name)

            separator = powerline.separator_thin
            separator_fg = Color.SEPARATOR_FG
            is_last_dir = (i == len(names) - 1)
            if requires_special_home_display(name) or is_last_dir:
                separator = None
                separator_fg = None

            powerline.append(' %s ' % maybe_shorten_name(name), fg, bg,
                             separator, separator_fg)

add_cwd_segment()
