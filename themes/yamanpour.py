class DefaultColor:
    """
    This class should have the default colors for every segment.
    Please test every new segment with this theme first.
    """
    USERNAME_FG = 15 # white
    USERNAME_BG = 31 # darkblue
    USERNAME_ROOT_BG = 160 # brightred

    HOSTNAME_FG = 220 # brightyellow
    HOSTNAME_BG = 166 #mediumorange

    HOME_SPECIAL_DISPLAY = True
    HOME_BG = 31  # blueish
    HOME_FG = 15  # white
    PATH_BG = 240  # gray4 (dark grey)
    PATH_FG = 250  # gray9 (light grey)
    CWD_FG = 254  # nearly-white grey
    SEPARATOR_FG = 244

    READONLY_BG = 124
    READONLY_FG = 254

    SSH_BG = 166 # mediumorange
    SSH_FG = 254

    REPO_CLEAN_BG = 148  # a light green color
    REPO_CLEAN_FG = 0  # black
    REPO_DIRTY_BG = 161  # pink/red
    REPO_DIRTY_FG = 15  # white

    JOBS_FG = 39
    JOBS_BG = 238

    CMD_PASSED_BG = 236
    CMD_PASSED_FG = 15
    CMD_FAILED_BG = 161
    CMD_FAILED_FG = 15

    SVN_CHANGES_BG = 148
    SVN_CHANGES_FG = 22  # dark green

    VIRTUAL_ENV_BG = 35  # a mid-tone green
    VIRTUAL_ENV_FG = 00

class Color(DefaultColor):
    """
    This subclass is required when the user chooses to use 'default' theme.
    Because the segments require a 'Color' class for every theme.
    """
    pass
