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
        if not (powerline.args.cwd_mode == 'dironly' or powerline.args.cwd_only):
            for n in names[:-1]:
                if n == '~' and Color.HOME_SPECIAL_DISPLAY:
                    powerline.append(' %s ' % n, Color.HOME_FG, Color.HOME_BG)
                else:
                    powerline.append(' %s ' % n, Color.PATH_FG, Color.PATH_BG,
                        powerline.separator_thin, Color.SEPARATOR_FG)

        if names[-1] == '~' and Color.HOME_SPECIAL_DISPLAY:
            powerline.append(' %s ' % names[-1], Color.HOME_FG, Color.HOME_BG)
        else:
            powerline.append(' %s ' % names[-1], Color.CWD_FG, Color.PATH_BG)

add_cwd_segment()
