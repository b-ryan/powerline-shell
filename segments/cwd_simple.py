import os

def add_cwd_segment():
    cwd = powerline.cwd or os.getenv('PWD')


    home = os.getenv('HOME')
    names = cwd.split(os.sep)
    chroot = os.getenv('SMSCHROOT')

    if names[0] == '': names = names[1:]
    max_depth = powerline.args.cwd_max_depth
    if len(names) > max_depth:
        names = names[:2] + [u'\u2026'] + names[2 - max_depth:]
    path = ''
    for i in range(len(names)):
        path += os.sep + names[i]
        if os.path.samefile(path, home):
            path = os.sep.join(['~'] + names[i+1:])
            break
    if not names[0]:
        path =  '/'

    #if (path == '/'): path = ''
    powerline.append(' %s ' % path, Color.PATH_FG, Color.PATH_BG)

add_cwd_segment()
