from powerline_shell.themes.default import DefaultColor


class Color(DefaultColor):
    USERNAME_FG = 15
    USERNAME_BG = 4
    USERNAME_ROOT_BG = 1

    HOSTNAME_FG = 15
    HOSTNAME_BG = 10

    HOME_SPECIAL_DISPLAY = False
    PATH_FG = 7
    PATH_BG = 10
    CWD_FG = 15
    SEPARATOR_FG = 14

    READONLY_BG = 1
    READONLY_FG = 7

    REPO_CLEAN_FG = 14
    REPO_CLEAN_BG = 0
    REPO_DIRTY_FG = 3
    REPO_DIRTY_BG = 0

    JOBS_FG = 4
    JOBS_BG = 8

    CMD_PASSED_FG = 15
    CMD_PASSED_BG = 2
    CMD_FAILED_FG = 15
    CMD_FAILED_BG = 1

    SVN_CHANGES_FG = REPO_DIRTY_FG
    SVN_CHANGES_BG = REPO_DIRTY_BG

    VIRTUAL_ENV_BG = 15
    VIRTUAL_ENV_FG = 2

    AWS_PROFILE_FG = 7
    AWS_PROFILE_BG = 2

    TIME_FG = 15
    TIME_BG = 10
