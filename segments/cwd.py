import os

def add_cwd_segment():
    home = os.getenv('HOME')
    cwd = powerline.cwd or os.getenv('PWD')
    cwd = cwd.decode('utf-8')

    if cwd.find(home) == 0:
        cwd = cwd.replace(home, '~', 1)

    if cwd[0] == '/':
        cwd = cwd[1:]

    names = cwd.split(os.sep)
    max_depth = powerline.args.cwd_max_depth
    if len(names) > max_depth:
        names = names[:2] + [u'\u2026'] + names[2 - max_depth:]

    if not powerline.args.cwd_only:
        for n in names[:-1]:
            powerline.append(' %s ' % n, Color.PATH_FG, Color.PATH_BG,
                    powerline.separator_thin, Color.SEPARATOR_FG)
    powerline.append(' %s ' % names[-1], Color.CWD_FG, Color.PATH_BG)

add_cwd_segment()
