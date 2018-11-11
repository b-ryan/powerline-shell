from powerline_shell.themes.default import DefaultColor

"""
absolute colors based on
https://github.com/morhetz/gruvbox/blob/master/colors/gruvbox.vim
"""
dark0 = 235
dark1 = 237
dark2 = 239
dark3 = 241
dark4 = 243

light0 = 229
light1 = 223
light2 = 250
light3 = 248
light4 = 246

dark_gray  = 245
light_gray = 244

neutral_red    = 124
neutral_green  = 106
neutral_yellow = 172
neutral_blue   = 66
neutral_purple = 132
neutral_aqua   = 72
neutral_orange = 166

bright_red    = 167
bright_green  = 142
bright_yellow = 214
bright_blue   = 109
bright_purple = 175
bright_aqua   = 108
bright_orange = 208

faded_red    = 88
faded_green  = 100
faded_yellow = 136
faded_blue   = 24
faded_purple = 96
faded_aqua   = 66
faded_orange = 130

class Color(DefaultColor):
    USERNAME_ROOT_BG = faded_red
    USERNAME_BG = dark2
    USERNAME_FG = bright_purple

    HOSTNAME_BG = dark1
    HOSTNAME_FG = bright_purple

    HOME_SPECIAL_DISPLAY = True
    HOME_BG = neutral_blue
    HOME_FG = light2
    PATH_BG = dark3
    PATH_FG = light3
    CWD_FG = light2
    SEPARATOR_FG = dark_gray

    READONLY_BG = bright_red
    READONLY_FG = light0

    SSH_BG = faded_purple
    SSH_FG = light0

    REPO_CLEAN_BG = faded_green
    REPO_CLEAN_FG = dark1
    REPO_DIRTY_BG = faded_orange
    REPO_DIRTY_FG = light0

    JOBS_FG = neutral_aqua
    JOBS_BG = dark1

    CMD_PASSED_FG = light4
    CMD_PASSED_BG = dark1
    CMD_FAILED_FG = light0
    CMD_FAILED_BG = neutral_red

    SVN_CHANGES_FG = REPO_DIRTY_FG
    SVN_CHANGES_BG = REPO_DIRTY_BG

    GIT_AHEAD_BG = dark2
    GIT_AHEAD_FG = light3
    GIT_BEHIND_BG = dark2
    GIT_BEHIND_FG = light3
    GIT_STAGED_BG = neutral_green
    GIT_STAGED_FG = light0
    GIT_NOTSTAGED_BG = neutral_orange
    GIT_NOTSTAGED_FG = light0
    GIT_UNTRACKED_BG = faded_red
    GIT_UNTRACKED_FG = light0
    GIT_CONFLICTED_BG = neutral_red
    GIT_CONFLICTED_FG = light0
    GIT_STASH_BG = neutral_yellow
    GIT_STASH_FG = dark0

    VIRTUAL_ENV_BG = faded_green
    VIRTUAL_ENV_FG = light0

    BATTERY_NORMAL_BG = neutral_green
    BATTERY_NORMAL_FG = dark2
    BATTERY_LOW_BG = neutral_red
    BATTERY_LOW_FG = light1

    AWS_PROFILE_FG = neutral_aqua
    AWS_PROFILE_BG = dark1

    TIME_FG = light2
    TIME_BG = dark4
