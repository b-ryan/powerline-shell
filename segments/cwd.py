import os

def get_short_path(cwd):
    home = os.getenv('HOME')
    names = cwd.split(os.sep)
    if names[0] == '': names = names[1:]
    path = ''
    for i in range(len(names)):
        path += os.sep + names[i]
        if os.path.samefile(path, home):
            return ['~'] + names[i+1:]
    if not names[0]:
        return ['/']
    return names

def add_cwd_segment():
    cwd = powerline.cwd or os.getenv('PWD')
    names = get_short_path(cwd.decode('utf-8'))

    # the current directory in one piece
    if powerline.args.cwd_split:
      powerline.append(' %s ' % cwd, Color.PATH_FG, Color.PATH_BG, powerline.separator, Color.SEPARATOR_FG)

    # the current directory in multiple pieces
    else:
      max_depth = powerline.args.cwd_max_depth
      if len(names) > max_depth:
          names = names[:2] + [u'\u2026'] + names[2 - max_depth:]

      # show only the last directory, not all of them
      if not powerline.args.cwd_only and not powerline.args.cwd_split:
          for n in names[:-1]:
              if n == '~' and Color.HOME_SPECIAL_DISPLAY:
                  powerline.append(' %s ' % n, Color.HOME_FG, Color.HOME_BG)
              else:
                  powerline.append(' %s ' % n, Color.PATH_FG, Color.PATH_BG,
                      powerline.separator_thin, Color.SEPARATOR_FG)

      # display home directory with special color
      if names[-1] == '~' and Color.HOME_SPECIAL_DISPLAY:
          powerline.append(' %s ' % names[-1], Color.HOME_FG, Color.HOME_BG)
      else:
          powerline.append(' %s ' % names[-1], Color.CWD_FG, Color.PATH_BG)

add_cwd_segment()
