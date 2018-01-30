from powerline_shell.themes.default import DefaultColor


class Color(DefaultColor):
    USERNAME_FG = 8
    USERNAME_BG = 251
    USERNAME_ROOT_BG = 209

    HOSTNAME_FG = 8
    HOSTNAME_BG = 7

    HOME_SPECIAL_DISPLAY = False
    PATH_BG = 15
    PATH_FG = 8
    CWD_FG = 8
    SEPARATOR_FG = 251

    READONLY_BG = 209
    READONLY_FG = 15

    REPO_CLEAN_BG = 150  # pale green
    REPO_CLEAN_FG = 235
    REPO_DIRTY_BG = 203  # pale red
    REPO_DIRTY_FG = 15

    JOBS_FG = 14
    JOBS_BG = 8

    CMD_PASSED_BG = 7
    CMD_PASSED_FG = 8
    CMD_FAILED_BG = 9
    CMD_FAILED_FG = 15

    SVN_CHANGES_BG = REPO_DIRTY_BG
    SVN_CHANGES_FG = REPO_DIRTY_FG

    VIRTUAL_ENV_BG = 150
    VIRTUAL_ENV_FG = 0

    AWS_PROFILE_FG = 0
    AWS_PROFILE_BG = 7

    TIME_FG = 8
    TIME_BG = 7
